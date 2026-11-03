"""Use real features and time sampling while replacing camera/ML I/O."""

from pathlib import Path
from contextlib import nullcontext
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import cv2

from hand_tracking import app, camera, landmarks
from hand_tracking.config import load_config


CONFIG = Path(__file__).resolve().parents[1] / "configs" / "default.json"


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.preview = getattr(app, "run_preview", None)
        self.assertTrue(callable(self.preview), "run_preview is not implemented")

    def test_missing_hand_resets_the_real_sequence_and_closes_resources(self):
        class Stream:
            count = 0
            closed = False

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.closed = True

            def read(self):
                timestamp = self.count * 50
                self.count += 1
                return camera.CameraFrame(timestamp, np.zeros((480, 640, 3), dtype=np.uint8))

        class Tracker:
            count = 0
            closed = False

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.closed = True

            def detect(self, image, timestamp_ms):
                self.count += 1
                if self.count == 31:
                    return landmarks.HandObservation(None, 0, None, "no_hand")
                points = np.tile([0.25, 0.5], (21, 1)).astype(np.float32)
                points[[5, 9, 13, 17], 0] = 0.375
                return landmarks.HandObservation(points, 1, "Right", None)

        stream, tracker = Stream(), Tracker()
        with patch.object(app, "Camera", return_value=stream), patch.object(
            app, "HandTracker", return_value=tracker
        ):
            summary = self.preview(load_config(CONFIG), headless=True, max_frames=35)
        self.assertEqual(summary["frames"], 35)
        self.assertEqual(summary["valid_hand_frames"], 34)
        self.assertEqual(summary["sequences_ready"], 1)
        self.assertEqual(summary["buffer_size"], 4)
        self.assertFalse(summary["control_enabled"])
        self.assertTrue(stream.closed)
        self.assertTrue(tracker.closed)

    def test_camera_failure_still_closes_camera_and_tracker(self):
        class Resource:
            closed = False

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.closed = True

            def read(self):
                raise camera.CameraError("Disconnected camera")

        stream, tracker = Resource(), Resource()
        with patch.object(app, "Camera", return_value=stream), patch.object(
            app, "HandTracker", return_value=tracker
        ):
            with self.assertRaises(camera.CameraError):
                self.preview(load_config(CONFIG), headless=True, max_frames=1)
        self.assertTrue(stream.closed)
        self.assertTrue(tracker.closed)

    def test_closed_native_window_property_error_is_a_normal_exit(self):
        image = np.zeros((480, 640, 3), dtype=np.uint8)
        stream = SimpleNamespace(read=lambda: camera.CameraFrame(0, image))
        tracker = SimpleNamespace(detect=lambda *_: landmarks.HandObservation(None, 0, None, "no_hand"))
        with patch.object(app, "Camera", return_value=nullcontext(stream)), patch.object(
            app, "HandTracker", return_value=nullcontext(tracker)
        ), patch("cv2.namedWindow"), patch("cv2.imshow"), patch("cv2.waitKey", return_value=-1), patch(
            "cv2.getWindowProperty", side_effect=cv2.error("Native window no longer exists")
        ), patch("cv2.destroyAllWindows"):
            try:
                summary = self.preview(load_config(CONFIG), max_frames=1)
            except cv2.error:
                self.fail("Closing the native window should end preview without an OpenCV traceback")
        self.assertEqual(summary["frames"], 1)


if __name__ == "__main__":
    unittest.main()
