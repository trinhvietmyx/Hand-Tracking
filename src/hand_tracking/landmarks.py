"""Synchronous MediaPipe Tasks adapter that accepts exactly one visible hand."""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class HandObservation:
    landmarks_xy: np.ndarray | None
    hand_count: int
    handedness: str | None
    reason: str | None


def observation_from_result(result) -> HandObservation:
    count = len(result.hand_landmarks)
    if count != 1:
        return HandObservation(None, count, None, "no_hand" if count == 0 else "multiple_hands")
    points = np.array([[point.x, point.y] for point in result.hand_landmarks[0]], dtype=np.float32)
    if points.shape != (21, 2) or not np.isfinite(points).all():
        return HandObservation(None, count, None, "invalid_landmarks")
    side = None
    if result.handedness and result.handedness[0]:
        side = result.handedness[0][0].category_name
    return HandObservation(points, count, side, None)


class HandTracker:
    def __init__(self, model_path: str | Path):
        model_path = Path(model_path)
        if not model_path.is_file():
            raise FileNotFoundError(
                f"Hand Landmarker model is missing: {model_path}. "
                "Follow assets/hand_landmarker/README.md to download it."
            )
        import mediapipe as mp

        self._mp = mp
        self._last_timestamp = -1
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
        )
        self._landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

    def __enter__(self):
        return self

    def detect(self, bgr_frame: np.ndarray, timestamp_ms: int) -> HandObservation:
        if self._landmarker is None:
            raise RuntimeError("Hand Landmarker is closed.")
        if timestamp_ms <= self._last_timestamp:
            raise ValueError("Hand Landmarker timestamps must be strictly increasing.")
        rgb = np.ascontiguousarray(cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB))
        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect_for_video(image, timestamp_ms)
        self._last_timestamp = timestamp_ms
        return observation_from_result(result)

    def close(self) -> None:
        if self._landmarker is not None:
            self._landmarker.close()
            self._landmarker = None

    def __exit__(self, exc_type, exc, traceback):
        self.close()
