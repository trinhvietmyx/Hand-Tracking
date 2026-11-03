"""Protect recordings, split boundaries and numeric training inputs."""

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from hand_tracking import dataset
from hand_tracking.config import load_config
from hand_tracking.labels import Gesture


CONFIG = Path(__file__).resolve().parents[1] / "configs" / "default.json"


def temporary_config(root):
    return replace(load_config(CONFIG), project_root=root, raw_dir=root / "data/raw",
                   processed_dir=root / "data/processed", output_dir=root / "outputs")


def example_clip():
    return dataset.RecordedClip(
        features=np.tile(np.arange(44, dtype=np.float32), (30, 1)),
        frames=[np.full((48, 64, 3), index * 5, dtype=np.uint8) for index in range(30)],
        frame_timestamps_ms=np.arange(30, dtype=np.float64) * 50,
        landmarks_xy=np.full((30, 21, 2), 0.25, dtype=np.float32),
        sample_timestamps_ms=np.arange(30, dtype=np.float64) * 50,
    )


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(dataset, "DatasetStore", None)), "DatasetStore is not implemented")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config = temporary_config(self.root)

    def test_real_video_and_npz_roundtrip_preserves_label_and_shape(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        record = store.save(example_clip(), Gesture.SWIPE_LEFT)
        X, y, records = dataset.load_split(self.config, "train")
        self.assertEqual(X.shape, (1, 30, 44))
        self.assertEqual(X.dtype, np.dtype("float32"))
        self.assertEqual(y.tolist(), [1])
        np.testing.assert_array_equal(X[0, 0], np.arange(44))
        self.assertEqual(records[0]["session_id"], "pilot_01")
        video = cv2.VideoCapture(str(self.root / record["raw_path"]))
        try:
            success, frame = video.read()
            self.assertTrue(success)
            self.assertEqual(frame.shape, (48, 64, 3))
            self.assertEqual(int(video.get(cv2.CAP_PROP_FRAME_COUNT)), 30)
        finally:
            video.release()
        with np.load(self.root / record["processed_path"], allow_pickle=False) as archive:
            np.testing.assert_array_equal(archive["frame_timestamps_ms"], np.arange(30) * 50)
            self.assertEqual(archive["landmarks_xy"].shape, (30, 21, 2))

    def test_resume_counts_saved_clips_without_overwriting_them(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        first = store.save(example_clip(), Gesture.BACKGROUND)
        original = (self.root / first["raw_path"]).read_bytes()
        resumed = dataset.DatasetStore(self.config, "pilot_01", "train")
        self.assertEqual(resumed.counts()["BACKGROUND"], 1)
        second = resumed.save(example_clip(), Gesture.BACKGROUND)
        self.assertNotEqual(first["clip_id"], second["clip_id"])
        self.assertEqual((self.root / first["raw_path"]).read_bytes(), original)
        self.assertEqual(resumed.counts()["BACKGROUND"], 2)

    def test_session_cannot_move_to_another_split_or_mirror_contract(self):
        dataset.DatasetStore(self.config, "pilot_01", "train")
        with self.assertRaises(dataset.DatasetError):
            dataset.DatasetStore(self.config, "pilot_01", "test")
        with self.assertRaises(dataset.DatasetError):
            dataset.DatasetStore(replace(self.config, mirror=False), "pilot_01", "train")

    def test_session_id_cannot_escape_data_directory(self):
        with self.assertRaises(dataset.DatasetError):
            dataset.DatasetStore(self.config, "../outside", "train")
        self.assertFalse((self.root / "outside").exists())

    def test_bad_features_are_rejected_without_creating_a_manifest(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        clip = example_clip()
        clip.features[0, 0] = np.nan
        with self.assertRaises(dataset.DatasetError):
            store.save(clip, Gesture.SWIPE_UP)
        self.assertFalse((self.root / "data/manifest.csv").exists())

    def test_failed_manifest_commit_keeps_previous_recordings(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        record = store.save(example_clip(), Gesture.SWIPE_UP)
        manifest = self.root / "data/manifest.csv"
        original = manifest.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("Simulated full disk")):
            with self.assertRaises(OSError):
                store.save(example_clip(), Gesture.SWIPE_DOWN)
        self.assertEqual(manifest.read_bytes(), original)
        self.assertTrue((self.root / record["raw_path"]).is_file())
        self.assertEqual(len(list(self.config.raw_dir.rglob("*.avi"))), 1)
        self.assertEqual(len(list(self.config.processed_dir.rglob("*.npz"))), 1)

    def test_loader_rejects_corrupt_or_incompatible_metadata(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        record = store.save(example_clip(), Gesture.SWIPE_RIGHT)
        path = self.root / record["processed_path"]
        with np.load(path, allow_pickle=False) as archive:
            values = {name: archive[name].copy() for name in archive.files}
        values["mirror"] = np.array(False)
        np.savez_compressed(path, **values)
        with self.assertRaises(dataset.DatasetError):
            dataset.load_split(self.config, "train")

    def test_loader_reports_broken_zip_as_a_dataset_error(self):
        store = dataset.DatasetStore(self.config, "pilot_01", "train")
        record = store.save(example_clip(), Gesture.SWIPE_RIGHT)
        (self.root / record["processed_path"]).write_bytes(b"PK\x03\x04broken archive")
        try:
            dataset.load_split(self.config, "train")
        except dataset.DatasetError:
            return
        except Exception as error:
            self.fail(f"Expected an actionable DatasetError, got {type(error).__name__}")
        self.fail("Broken archive was accepted")


if __name__ == "__main__":
    unittest.main()
