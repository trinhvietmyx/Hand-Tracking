"""Removal must preserve unrelated recordings and support rollback/restore."""

import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from hand_tracking import dataset_cleanup as cleanup
from hand_tracking.dataset import DatasetError, DatasetStore, MANIFEST_FIELDS, load_split
from hand_tracking.labels import Gesture
from test_dataset import example_clip, temporary_config


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(cleanup, "remove_recordings", None)), "Removal is not implemented")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config = temporary_config(self.root)
        self.store = DatasetStore(self.config, "pilot_01", "train")
        self.left = self.store.save(example_clip(), Gesture.SWIPE_LEFT)
        self.background = self.store.save(example_clip(), Gesture.BACKGROUND)
        other = DatasetStore(self.config, "train_02", "train")
        self.other = other.save(example_clip(), Gesture.SWIPE_LEFT)
        self.manifest = self.root / "data/manifest.csv"

    def remove(self, **kwargs):
        return cleanup.remove_recordings(self.config, "pilot_01", "train", Gesture.SWIPE_LEFT, **kwargs)

    def test_default_preview_changes_no_files_or_manifest(self):
        original = self.manifest.read_bytes()
        result = self.remove()
        self.assertEqual(result["matched"], 1)
        self.assertFalse(result["applied"])
        self.assertEqual(self.manifest.read_bytes(), original)
        self.assertTrue((self.root / self.left["raw_path"]).is_file())
        self.assertFalse((self.root / "data/removed").exists())

    def test_apply_moves_only_matching_session_and_label_to_backup(self):
        result = self.remove(apply=True)
        self.assertEqual(result["removed"], 1)
        self.assertFalse((self.root / self.left["raw_path"]).exists())
        self.assertFalse((self.root / self.left["processed_path"]).exists())
        self.assertTrue((self.root / self.background["raw_path"]).is_file())
        self.assertTrue((self.root / self.other["raw_path"]).is_file())
        backup = Path(result["backup_dir"])
        self.assertEqual(len(list((backup / "files").iterdir())), 2)
        self.assertEqual(self.store.counts()["SWIPE_LEFT"], 0)
        self.assertEqual(load_split(self.config, "train")[1].tolist(), [0, 1])

    def test_last_removes_only_the_latest_matching_clip(self):
        latest = self.store.save(example_clip(), Gesture.SWIPE_LEFT)
        result = self.remove(last=True, apply=True)
        self.assertEqual(result["clip_ids"], [latest["clip_id"]])
        self.assertTrue((self.root / self.left["raw_path"]).is_file())
        self.assertEqual(self.store.counts()["SWIPE_LEFT"], 1)

    def test_manifest_commit_failure_puts_files_back(self):
        original = self.manifest.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("Cannot commit manifest")):
            with self.assertRaises(OSError):
                self.remove(apply=True)
        self.assertEqual(self.manifest.read_bytes(), original)
        self.assertTrue((self.root / self.left["raw_path"]).is_file())
        self.assertTrue((self.root / self.left["processed_path"]).is_file())

    def test_unexpected_source_path_is_refused_before_any_move(self):
        outside = self.root / "outside.avi"
        outside.write_bytes(b"Must not be moved")
        with self.manifest.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        rows[0]["raw_path"] = str(outside)
        with self.manifest.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaises(DatasetError):
            self.remove(apply=True)
        self.assertEqual(outside.read_bytes(), b"Must not be moved")
        self.assertTrue((self.root / self.left["processed_path"]).is_file())

    def test_restore_merges_with_new_recordings_instead_of_replacing_manifest(self):
        result = self.remove(apply=True)
        new = self.store.save(example_clip(), Gesture.SWIPE_LEFT)
        restored = cleanup.restore_recordings(self.config, result["removal_id"], apply=True)
        self.assertEqual(restored["restored"], 1)
        self.assertTrue((self.root / new["raw_path"]).is_file())
        self.assertTrue((self.root / self.left["raw_path"]).is_file())
        self.assertEqual(self.store.counts()["SWIPE_LEFT"], 2)
        self.assertEqual(load_split(self.config, "train")[0].shape, (4, 30, 44))

    def test_restore_preview_is_read_only_and_collision_is_refused(self):
        result = self.remove(apply=True)
        preview = cleanup.restore_recordings(self.config, result["removal_id"])
        self.assertFalse(preview["applied"])
        self.assertFalse((self.root / self.left["raw_path"]).exists())
        original = self.root / self.left["raw_path"]
        original.write_bytes(b"A newer file at the original path")
        with self.assertRaises(DatasetError):
            cleanup.restore_recordings(self.config, result["removal_id"], apply=True)
        self.assertEqual(original.read_bytes(), b"A newer file at the original path")


if __name__ == "__main__":
    unittest.main()
