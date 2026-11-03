"""Clip timing and interactive collection with fake camera/tracker I/O."""

from contextlib import nullcontext
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from hand_tracking import collection, dataset
from hand_tracking.camera import CameraFrame
from hand_tracking.config import load_config
from hand_tracking.landmarks import HandObservation
from hand_tracking.labels import Gesture
from test_dataset import temporary_config


CONFIG = Path(__file__).resolve().parents[1] / "configs" / "default.json"


def one_hand():
    points = np.tile([0.25, 0.5], (21, 1)).astype(np.float32)
    points[[5, 9, 13, 17], 0] = 0.375
    return HandObservation(points, 1, "Right", None)


def frame_at(timestamp):
    return CameraFrame(timestamp, np.zeros((48, 64, 3), dtype=np.uint8))


class ClipAttemptTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(collection, "ClipAttempt", None)), "ClipAttempt is not implemented")
        self.config = load_config(CONFIG)

    def test_complete_clip_keeps_clean_frames_before_overlay(self):
        attempt = collection.ClipAttempt(self.config)
        first = frame_at(3000)
        self.assertIsNone(attempt.push(first, one_hand()))
        first.image[:] = 255
        for index in range(1, 29):
            self.assertIsNone(attempt.push(frame_at(3000 + index * 50), one_hand()))
        clip = attempt.push(frame_at(4450), one_hand())
        self.assertEqual(clip.features.shape, (30, 44))
        self.assertEqual(len(clip.frames), 30)
        self.assertEqual(int(clip.frames[0].max()), 0)
        np.testing.assert_allclose(clip.frame_timestamps_ms, np.arange(30) * 50)

    def test_missing_hand_or_long_gap_rejects_the_whole_attempt(self):
        for timestamp, observation in ((50, HandObservation(None, 0, None, "no_hand")),
                                       (50, HandObservation(None, 2, None, "multiple_hands")),
                                       (150, one_hand())):
            attempt = collection.ClipAttempt(self.config)
            attempt.push(frame_at(0), one_hand())
            with self.subTest(timestamp=timestamp), self.assertRaises(collection.ClipRejected):
                attempt.push(frame_at(timestamp), observation)

    def test_irregular_camera_frames_preserve_real_and_grid_times(self):
        attempt = collection.ClipAttempt(self.config)
        for timestamp in range(0, 1441, 80):
            self.assertIsNone(attempt.push(frame_at(timestamp), one_hand()))
        clip = attempt.push(frame_at(1530), one_hand())
        self.assertEqual(clip.frame_timestamps_ms[-1], 1530)
        np.testing.assert_allclose(clip.sample_timestamps_ms, np.arange(30) * 50 + 50)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(collection, "collect_clips", None)), "collect_clips is not implemented")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config = temporary_config(self.root)

    def run_collector(self, keys, count=1, max_frames=40, missing_at=None, countdown_seconds=0):
        clock = iter(range(0, 10000, 50))
        stream = SimpleNamespace(read=lambda: frame_at(next(clock)))
        tracker = SimpleNamespace(detect=lambda image, timestamp: (
            HandObservation(None, 0, None, "no_hand") if timestamp == missing_at else one_hand()
        ))
        with patch.object(collection, "Camera", return_value=nullcontext(stream)), patch.object(
            collection, "HandTracker", return_value=nullcontext(tracker)
        ), patch.object(collection, "poll_key", side_effect=keys), patch("cv2.namedWindow"), patch(
            "cv2.imshow"
        ), patch("cv2.destroyAllWindows"):
            return collection.collect_clips(self.config, "pilot_01", "train", count,
                                            [Gesture.BACKGROUND], countdown_seconds=countdown_seconds,
                                            max_frames=max_frames)

    def test_does_not_record_until_space_is_pressed(self):
        summary = self.run_collector([-1] * 4, max_frames=4)
        self.assertEqual(summary["saved_this_run"], 0)
        self.assertFalse((self.root / "data/manifest.csv").exists())

    def test_space_records_one_valid_clip_and_stops_at_target(self):
        summary = self.run_collector([32] + [-1] * 40)
        self.assertEqual(summary["saved_this_run"], 1)
        self.assertTrue(summary["completed"])
        X, y, _ = dataset.load_split(self.config, "train")
        self.assertEqual(X.shape, (1, 30, 44))
        self.assertEqual(y.tolist(), [0])

    def test_countdown_frames_are_not_saved_as_a_clip(self):
        summary = self.run_collector([32] + [-1] * 20, max_frames=20, countdown_seconds=2)
        self.assertEqual(summary["saved_this_run"], 0)
        self.assertFalse((self.root / "data/manifest.csv").exists())

    def test_lost_hand_requires_retry_and_saves_only_the_new_attempt(self):
        keys = [32] + [-1] * 10 + [32] + [-1] * 50
        summary = self.run_collector(keys, max_frames=60, missing_at=500)
        self.assertEqual(summary["rejected_attempts"], 1)
        self.assertEqual(summary["saved_this_run"], 1)
        self.assertEqual(len(list(self.config.processed_dir.rglob("*.npz"))), 1)

    def test_quit_discards_an_unfinished_attempt(self):
        summary = self.run_collector([32] + [-1] * 8 + [ord("q")])
        self.assertEqual(summary["saved_this_run"], 0)
        self.assertTrue(summary["aborted"])
        self.assertFalse((self.root / "data/manifest.csv").exists())

    def test_completed_session_does_not_open_camera_again(self):
        self.run_collector([32] + [-1] * 40)
        with patch.object(collection, "Camera", side_effect=AssertionError("Camera should stay closed")):
            summary = collection.collect_clips(self.config, "pilot_01", "train", 1, [Gesture.BACKGROUND])
        self.assertTrue(summary["completed"])
        self.assertEqual(summary["saved_this_run"], 0)


if __name__ == "__main__":
    unittest.main()
