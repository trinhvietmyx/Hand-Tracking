"""Small on-disk dataset: separate sessions, clean video, numeric NPZ and manifest."""

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from uuid import uuid4
from zipfile import BadZipFile

import cv2
import numpy as np

from .config import ProjectConfig
from .features import FEATURE_VERSION
from .labels import CLASS_NAMES, Gesture


SPLITS = ("train", "validation", "test")
MANIFEST_FIELDS = ("clip_id", "session_id", "split", "label_id", "label", "raw_path", "processed_path", "created_at")


class DatasetError(ValueError):
    """A recording or dataset does not satisfy the current contract."""


@dataclass
class RecordedClip:
    features: np.ndarray
    frames: list[np.ndarray]
    frame_timestamps_ms: np.ndarray
    landmarks_xy: np.ndarray
    sample_timestamps_ms: np.ndarray


def _contract(config: ProjectConfig) -> dict:
    return {"feature_version": FEATURE_VERSION, "sequence_length": config.sequence_length,
            "feature_dim": config.feature_dim, "sample_rate_hz": config.sample_rate_hz,
            "mirror": config.mirror, "class_names": list(CLASS_NAMES)}


def _read_manifest(config: ProjectConfig) -> list[dict]:
    path = config.project_root / "data/manifest.csv"
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(MANIFEST_FIELDS):
            raise DatasetError("Invalid manifest header.")
        rows = list(reader)
    sessions, clip_ids = {}, set()
    for row in rows:
        try:
            label = Gesture(int(row["label_id"]))
            valid = (row["split"] in SPLITS and row["label"] == label.name
                     and all(row.get(field) for field in MANIFEST_FIELDS))
        except (ValueError, TypeError):
            valid = False
        if not valid or row["clip_id"] in clip_ids:
            raise DatasetError("Invalid or duplicate manifest record.")
        clip_ids.add(row["clip_id"])
        previous_split = sessions.setdefault(row["session_id"], row["split"])
        if previous_split != row["split"]:
            raise DatasetError(f"Session {row['session_id']} occurs in multiple splits.")
    return rows


def _validate_arrays(features, times, xy, sample_times, config):
    if features.shape != (config.sequence_length, config.feature_dim) or not np.isfinite(features).all():
        raise DatasetError("Expected a complete finite feature sequence.")
    if (times.ndim != 1 or not len(times) or not np.isfinite(times).all()
            or times[0] != 0 or np.any(np.diff(times) <= 0)):
        raise DatasetError("Invalid original frame timestamps.")
    if xy.shape != (len(times), 21, 2) or not np.isfinite(xy).all():
        raise DatasetError("Invalid original xy landmarks.")
    if (sample_times.shape != (config.sequence_length,) or not np.isfinite(sample_times).all()
            or sample_times[0] < 0 or sample_times[-1] > times[-1] + 1e-6
            or not np.allclose(np.diff(sample_times), 1000 / config.sample_rate_hz)):
        raise DatasetError("Invalid feature sampling grid.")


class DatasetStore:
    """One collector process at a time; unique files and atomic manifest replacement."""

    def __init__(self, config: ProjectConfig, session_id: str, split: str):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", session_id):
            raise DatasetError("session_id must use 1-64 letters, digits, underscores or hyphens.")
        if split not in SPLITS:
            raise DatasetError("split must be train, validation or test.")
        self.config, self.session_id, self.split = config, session_id, split
        self.manifest = config.project_root / "data/manifest.csv"
        session_path = config.project_root / "data/sessions" / f"{session_id}.json"
        contract = {**_contract(config), "session_id": session_id, "split": split}
        for row in _read_manifest(config):
            if row["session_id"] == session_id and row["split"] != split:
                raise DatasetError("Session already belongs to a different split.")
        if session_path.exists():
            existing = json.loads(session_path.read_text(encoding="utf-8"))
            if existing != contract:
                raise DatasetError("Session split or preprocessing contract changed; use a new session_id.")
        else:
            session_path.parent.mkdir(parents=True, exist_ok=True)
            with session_path.open("x", encoding="utf-8") as stream:
                json.dump(contract, stream, indent=2)

    def counts(self) -> dict[str, int]:
        counts = {name: 0 for name in CLASS_NAMES}
        for row in _read_manifest(self.config):
            if row["session_id"] == self.session_id and row["split"] == self.split:
                counts[row["label"]] += 1
        return counts

    def save(self, clip: RecordedClip, label: Gesture) -> dict:
        label = Gesture(label)
        _validate_arrays(clip.features, clip.frame_timestamps_ms, clip.landmarks_xy,
                         clip.sample_timestamps_ms, self.config)
        if not clip.frames or len(clip.frames) != len(clip.frame_timestamps_ms):
            raise DatasetError("Frame images and timestamps do not match.")
        shape = clip.frames[0].shape
        if (len(shape) != 3 or shape[2] != 3 or any(
                image.shape != shape or image.dtype != np.uint8 for image in clip.frames)):
            raise DatasetError("Video frames must have one fixed uint8 BGR shape.")
        height, width = shape[:2]
        clip_id = uuid4().hex
        stem = f"{self.session_id}_{clip_id}"
        raw = self.config.raw_dir / self.split / label.name / f"{stem}.avi"
        processed = self.config.processed_dir / self.split / label.name / f"{stem}.npz"
        raw.parent.mkdir(parents=True, exist_ok=True)
        processed.parent.mkdir(parents=True, exist_ok=True)
        raw_temp = raw.with_name(f".{stem}.pending.avi")
        processed_temp = processed.with_name(f".{stem}.pending.npz")
        manifest_temp = self.manifest.with_name(f".manifest_{clip_id}.tmp")

        def reference(path):
            try:
                return path.relative_to(self.config.project_root).as_posix()
            except ValueError:
                return str(path)

        record = {"clip_id": clip_id, "session_id": self.session_id, "split": self.split,
                  "label_id": str(int(label)), "label": label.name, "raw_path": reference(raw),
                  "processed_path": reference(processed), "created_at": datetime.now(timezone.utc).isoformat()}
        created = []
        try:
            fps = ((len(clip.frames) - 1) * 1000 / clip.frame_timestamps_ms[-1]
                   if len(clip.frames) > 1 else self.config.sample_rate_hz)
            writer = cv2.VideoWriter(str(raw_temp), cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))
            try:
                if not writer.isOpened():
                    raise DatasetError("Cannot create an MJPG/AVI video writer.")
                for image in clip.frames:
                    writer.write(image)
            finally:
                writer.release()
            probe = cv2.VideoCapture(str(raw_temp))
            try:
                readable, _ = probe.read()
                if not readable or int(probe.get(cv2.CAP_PROP_FRAME_COUNT)) != len(clip.frames):
                    raise DatasetError("Video encoder did not save every frame.")
            finally:
                probe.release()
            with processed_temp.open("xb") as stream:
                np.savez_compressed(
                    stream, features=clip.features.astype(np.float32), label=int(label),
                    session_id=self.session_id, split=self.split, source_clip=record["raw_path"],
                    frame_timestamps_ms=clip.frame_timestamps_ms, landmarks_xy=clip.landmarks_xy,
                    sample_timestamps_ms=clip.sample_timestamps_ms, frame_width=width, frame_height=height,
                    **_contract(self.config),
                )
            for temporary, final in ((raw_temp, raw), (processed_temp, processed)):
                if final.exists():
                    raise DatasetError("Recording ID collision; existing files were not overwritten.")
                temporary.rename(final)
                created.append(final)
            rows = _read_manifest(self.config)
            with manifest_temp.open("x", newline="", encoding="utf-8") as stream:
                manifest_writer = csv.DictWriter(stream, fieldnames=MANIFEST_FIELDS)
                manifest_writer.writeheader()
                manifest_writer.writerows([*rows, record])
            manifest_temp.replace(self.manifest)
        except BaseException:
            for path in [*created, raw_temp, processed_temp, manifest_temp]:
                path.unlink(missing_ok=True)
            raise
        return record


def load_split(config: ProjectConfig, split: str):
    """Load verified numeric samples; no webcam, pickle or implicit train/test shuffle."""
    if split not in SPLITS:
        raise DatasetError("Unknown split.")
    rows = [row for row in _read_manifest(config) if row["split"] == split]
    if not rows:
        raise DatasetError(f"No clips for split '{split}'. Collect labelled data first.")
    inputs, targets = [], []
    for row in rows:
        path = config.project_root / row["processed_path"]
        try:
            if not (config.project_root / row["raw_path"]).is_file():
                raise DatasetError(f"Original video is missing for {row['clip_id']}.")
            with path.open("rb") as source, np.load(source, allow_pickle=False) as archive:
                for name, expected in _contract(config).items():
                    actual = archive[name].tolist()
                    if actual != expected:
                        raise DatasetError(f"Incompatible {name} in {path.name}.")
                if (archive["label"].item() != int(row["label_id"])
                        or archive["session_id"].item() != row["session_id"]
                        or archive["split"].item() != split
                        or archive["source_clip"].item() != row["raw_path"]):
                    raise DatasetError(f"NPZ metadata differs from manifest: {path.name}.")
                features = np.asarray(archive["features"], dtype=np.float32)
                _validate_arrays(features, archive["frame_timestamps_ms"], archive["landmarks_xy"],
                                 archive["sample_timestamps_ms"], config)
                inputs.append(features)
                targets.append(int(row["label_id"]))
        except (OSError, KeyError, ValueError, BadZipFile, EOFError) as error:
            raise DatasetError(f"Cannot load {path}: {error}") from error
    return np.stack(inputs), np.asarray(targets, dtype=np.int64), rows
