"""Reversible removal of mistaken recordings and restoration of removed records."""

import csv
import json
from pathlib import Path
import re
import shutil
from uuid import uuid4

from .dataset import DatasetError, MANIFEST_FIELDS, SPLITS, _contract, _read_manifest
from .labels import Gesture


def _record_paths(config, row):
    """Validate exact generated paths before a recording is moved anywhere."""
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", row["session_id"])
            or not re.fullmatch(r"[0-9a-f]{32}", row["clip_id"])
            or row["split"] not in SPLITS
            or Gesture(int(row["label_id"])).name != row["label"]):
        raise DatasetError("Invalid recording identity in removal metadata.")
    paths = []
    for field, root, extension in (("raw_path", config.raw_dir, "avi"),
                                   ("processed_path", config.processed_dir, "npz")):
        root = root.resolve()
        actual = (config.project_root / row[field]).resolve()
        expected = (root / row["split"] / row["label"]
                    / f"{row['session_id']}_{row['clip_id']}.{extension}").resolve()
        if actual != expected or not actual.is_relative_to(root):
            raise DatasetError(f"Unexpected {field}; refusing to move files outside the recording scope.")
        paths.append(actual)
    return paths


def _backup_folder(config, removal_id):
    if not re.fullmatch(r"[0-9a-f]{32}", removal_id):
        raise DatasetError("Invalid backup ID.")
    root = config.project_root.resolve()
    folder = (root / "data/removed" / removal_id).resolve()
    if not folder.is_relative_to(root):
        raise DatasetError("Backup directory must stay within this project.")
    return folder


def _backup_file(folder, clip_id, extension):
    path = (folder / "files" / f"{clip_id}.{extension}").resolve()
    if not path.is_relative_to(folder):
        raise DatasetError("Backup file escaped its backup directory.")
    return path


def _write_csv(path, rows):
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _move_and_commit(config, moves, rows):
    """Roll back this operation's file moves if the atomic manifest commit fails."""
    manifest = config.project_root / "data/manifest.csv"
    temporary = manifest.with_name(f".manifest_{uuid4().hex}.tmp")
    moved = []
    try:
        for source, target in moves:
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
            moved.append((source, target))
        _write_csv(temporary, rows)
        temporary.replace(manifest)
    except BaseException:
        for source, target in reversed(moved):
            target.rename(source)
        raise
    finally:
        temporary.unlink(missing_ok=True)


def remove_recordings(config, session_id, split, label, last=False, apply=False):
    """Preview or move only the selected session/label recordings to a backup."""
    if (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", session_id)
            or split not in SPLITS):
        raise DatasetError("Invalid session_id or split.")
    label = Gesture(label)
    rows = _read_manifest(config)
    selected = [row for row in rows if row["session_id"] == session_id
                and row["split"] == split and row["label"] == label.name]
    if last:
        selected = selected[-1:]
    report = {"status": "dry_run", "session_id": session_id, "split": split, "label": label.name,
              "matched": len(selected), "clip_ids": [row["clip_id"] for row in selected],
              "applied": False, "removed": 0}
    removal_id = uuid4().hex
    folder = _backup_folder(config, removal_id)
    moves = []
    for row in selected:
        for source, extension in zip(_record_paths(config, row), ("avi", "npz")):
            target = _backup_file(folder, row["clip_id"], extension)
            if not source.is_file() or target.exists():
                raise DatasetError(f"Recording is missing or backup target already exists: {source}")
            if source.drive.lower() != target.drive.lower():
                raise DatasetError("Recording and backup must be on the same drive for reversible moves.")
            moves.append((source, target))
    if not apply or not selected:
        return report
    folder.mkdir(parents=True)
    shutil.copyfile(config.project_root / "data/manifest.csv", folder / "manifest_before.csv")
    _write_csv(folder / "removed.csv", selected)
    selected_ids = {row["clip_id"] for row in selected}
    remaining = [row for row in rows if row["clip_id"] not in selected_ids]
    _move_and_commit(config, moves, remaining)
    return {**report, "status": "removed", "applied": True, "removed": len(selected),
            "removal_id": removal_id, "backup_dir": str(folder)}


def restore_recordings(config, removal_id, apply=False):
    """Restore removed entries by merging them with any newly collected samples."""
    folder = _backup_folder(config, removal_id)
    removed_csv = folder / "removed.csv"
    if not removed_csv.is_file():
        raise DatasetError("Backup metadata was not found.")
    with removed_csv.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(MANIFEST_FIELDS):
            raise DatasetError("Invalid backup manifest header.")
        selected = list(reader)
    if not selected:
        raise DatasetError("Backup contains no records.")
    rows = _read_manifest(config)
    active_ids = {row["clip_id"] for row in rows}
    moves, selected_ids = [], set()
    for row in selected:
        targets = _record_paths(config, row)
        if row["clip_id"] in active_ids or row["clip_id"] in selected_ids:
            raise DatasetError("A backup clip is already active or duplicated; no files were overwritten.")
        selected_ids.add(row["clip_id"])
        session_path = config.project_root / "data/sessions" / f"{row['session_id']}.json"
        expected = {**_contract(config), "session_id": row["session_id"], "split": row["split"]}
        if not session_path.is_file() or json.loads(session_path.read_text(encoding="utf-8")) != expected:
            raise DatasetError("Session preprocessing metadata is missing or incompatible.")
        if any(active["session_id"] == row["session_id"] and active["split"] != row["split"] for active in rows):
            raise DatasetError("Restoring would place a session in multiple splits.")
        for target, extension in zip(targets, ("avi", "npz")):
            source = _backup_file(folder, row["clip_id"], extension)
            if not source.is_file() or target.exists():
                raise DatasetError("Backup files are missing or an original path already exists; refusing overwrite.")
            moves.append((source, target))
    report = {"status": "dry_run", "removal_id": removal_id, "matched": len(selected),
              "applied": False, "restored": 0}
    if not apply:
        return report
    _move_and_commit(config, moves, [*rows, *selected])
    return {**report, "status": "restored", "applied": True, "restored": len(selected)}
