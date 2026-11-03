"""Test the hardware boundaries with controlled frames, not a real webcam."""

from dataclasses import replace
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from hand_tracking import camera, landmarks
from hand_tracking.config import load_config


CONFIG = Path(__file__).resolve().parents[1] / "configs" / "default.json"


class FakeCapture:
    def __init__(self, frames=(), opened=True):
        self.frames = iter(frames)
        self.opened = opened
        self.released = False

    def isOpened(self):
        return self.opened

    def set(self, prop, value):
        return True

    def read(self):
        frame = next(self.frames, None)
        return frame is not None, frame

    def release(self):
        self.released = True


def hand_result(count=1, point_count=21):
    points = [SimpleNamespace(x=0.25, y=0.5, z=0.0) for _ in range(point_count)]
    category = SimpleNamespace(category_name="Right", score=0.99, index=1)
    return SimpleNamespace(
        hand_landmarks=[points for _ in range(count)],
        hand_world_landmarks=[points for _ in range(count)],
        handedness=[[category] for _ in range(count)],
    )


class CameraTests(unittest.TestCase):
    def setUp(self):
        self.camera_type = getattr(camera, "Camera", None)
        self.assertTrue(callable(self.camera_type), "Camera is not implemented")

    def test_applies_mirror_once_and_releases_after_read(self):
        image = np.array([[[1, 2, 3], [4, 5, 6]]], dtype=np.uint8)
        capture = FakeCapture([image])
        with patch("cv2.VideoCapture", return_value=capture):
            with self.camera_type(load_config(CONFIG)) as stream:
                frame = stream.read()
                np.testing.assert_array_equal(frame.image[0, 0], [4, 5, 6])
        self.assertTrue(capture.released)

    def test_release_camera_when_frame_read_fails(self):
        capture = FakeCapture()
        with patch("cv2.VideoCapture", return_value=capture):
            with self.assertRaises(camera.CameraError):
                with self.camera_type(load_config(CONFIG)) as stream:
                    stream.read()
        self.assertTrue(capture.released)

    def test_release_unavailable_camera(self):
        capture = FakeCapture(opened=False)
        with patch("cv2.VideoCapture", return_value=capture):
            with self.assertRaises(camera.CameraError):
                with self.camera_type(load_config(CONFIG)):
                    self.fail("An unavailable camera must not enter the context")
        self.assertTrue(capture.released)

    def test_timestamps_remain_strictly_increasing(self):
        image = np.zeros((2, 2, 3), dtype=np.uint8)
        capture = FakeCapture([image, image])
        with patch("cv2.VideoCapture", return_value=capture), patch.object(
            camera, "monotonic_ns", return_value=1_000_000
        ):
            with self.camera_type(replace(load_config(CONFIG), mirror=False)) as stream:
                first = stream.read()
                second = stream.read()
        self.assertGreater(second.timestamp_ms, first.timestamp_ms)


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.parse = getattr(landmarks, "observation_from_result", None)
        self.assertTrue(callable(self.parse), "observation_from_result is not implemented")

    def test_single_hand_contains_21_finite_xy_points(self):
        observation = self.parse(hand_result())
        self.assertEqual(observation.landmarks_xy.shape, (21, 2))
        self.assertEqual(observation.handedness, "Right")
        self.assertIsNone(observation.reason)

    def test_no_hand_or_two_hands_are_rejected(self):
        for count, reason in ((0, "no_hand"), (2, "multiple_hands")):
            with self.subTest(count=count):
                observation = self.parse(hand_result(count=count))
                self.assertIsNone(observation.landmarks_xy)
                self.assertEqual(observation.reason, reason)

    def test_incomplete_landmarks_are_rejected(self):
        observation = self.parse(hand_result(point_count=20))
        self.assertIsNone(observation.landmarks_xy)
        self.assertEqual(observation.reason, "invalid_landmarks")


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tracker_type = getattr(landmarks, "HandTracker", None)
        self.assertTrue(callable(self.tracker_type), "HandTracker is not implemented")

    def test_converts_bgr_to_rgb_and_releases_landmarker(self):
        import mediapipe as mp

        class Engine:
            closed = False

            def detect_for_video(self, image, timestamp_ms):
                self.pixel = image.numpy_view()[0, 0].tolist()
                self.timestamp = timestamp_ms
                return hand_result(count=0)

            def close(self):
                self.closed = True

        engine = Engine()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.task"
            path.write_bytes(b"test model; inference is replaced at the library boundary")
            with patch.object(mp.tasks.vision.HandLandmarker, "create_from_options", return_value=engine):
                with self.tracker_type(path) as tracker:
                    tracker.detect(np.array([[[10, 20, 30]]], dtype=np.uint8), 125)
        self.assertEqual(engine.pixel, [30, 20, 10])
        self.assertEqual(engine.timestamp, 125)
        self.assertTrue(engine.closed)


if __name__ == "__main__":
    unittest.main()
