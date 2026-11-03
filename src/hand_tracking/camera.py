"""OpenCV camera lifetime, monotonic timestamps and a single mirror transform."""

from dataclasses import dataclass
from time import monotonic_ns

import cv2
import numpy as np

from .config import ProjectConfig


class CameraError(RuntimeError):
    """Camera could not be opened or stopped supplying valid frames."""


@dataclass(frozen=True)
class CameraFrame:
    timestamp_ms: int
    image: np.ndarray


class Camera:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self._capture = None
        self._last_timestamp = -1

    def __enter__(self):
        self._capture = cv2.VideoCapture(self.config.camera_index)
        if not self._capture.isOpened():
            self.close()
            raise CameraError(
                f"Cannot open camera {self.config.camera_index}. "
                "Check the camera index, Windows camera permissions or other apps using it."
            )
        try:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.frame_width)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)
        except Exception:
            self.close()
            raise
        return self

    def read(self) -> CameraFrame:
        if self._capture is None:
            raise CameraError("Camera is not open.")
        success, image = self._capture.read()
        if not success or image is None or image.ndim != 3 or image.shape[2] != 3:
            raise CameraError("Camera stopped supplying valid BGR frames.")
        if self.config.mirror:
            image = cv2.flip(image, 1)
        timestamp = max(monotonic_ns() // 1_000_000, self._last_timestamp + 1)
        self._last_timestamp = timestamp
        return CameraFrame(timestamp, image)

    def close(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def __exit__(self, exc_type, exc, traceback):
        self.close()
