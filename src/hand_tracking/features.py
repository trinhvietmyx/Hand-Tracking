"""Shared 2D hand features and timestamp-based sampling for data and runtime."""

from collections import deque
import math

import numpy as np

FEATURE_VERSION = "xy_palm_v1"


def extract_features(landmarks_xy, frame_size: tuple[int, int]) -> np.ndarray:
    """Return 42 local xy coordinates plus two global wrist coordinates.

    frame_size is (width, height). Both axes are first expressed in units
    of the longer image side, so palm shape is not stretched by aspect ratio.
    The returned vector is float32, with landmark order unchanged.
    """
    points = np.asarray(landmarks_xy, dtype=np.float64)
    if points.shape != (21, 2) or not np.isfinite(points).all():
        raise ValueError("Expected 21 finite xy landmarks.")
    width, height = frame_size
    if not all(math.isfinite(value) and value > 0 for value in (width, height)):
        raise ValueError("Frame width and height must be positive and finite.")
    points = points * np.array([width, height]) / max(width, height)
    wrist = points[0]
    scale = float(np.median(np.linalg.norm(points[[5, 9, 13, 17]] - wrist, axis=1)))
    if scale <= 1e-6:
        raise ValueError("Palm size is too small to normalize.")
    local = (points - wrist) / scale
    result = np.concatenate((local.reshape(42), wrist)).astype(np.float32)
    if not np.isfinite(result).all():
        raise ValueError("Hand features are not finite.")
    return result


class SequenceBuffer:
    """Sample an observed trajectory onto a fixed grid without future frames.

    push returns [length,44] only when a new grid sample completes/updates a
    full sequence. No hand, invalid data or a long tracking gap clears history.
    Short gaps are interpolated only once both endpoints have been received.
    """

    def __init__(self, length: int = 30, sample_rate_hz: int = 20, max_gap_ms: int = 100):
        if length < 1 or sample_rate_hz <= 0 or max_gap_ms <= 0:
            raise ValueError("Length, sample rate and maximum gap must be positive.")
        self.length = length
        self._step_ms = 1000.0 / sample_rate_hz
        self._max_gap_ms = max_gap_ms
        self._samples = deque(maxlen=length)
        self.reset()

    @property
    def size(self) -> int:
        return len(self._samples)

    def reset(self) -> None:
        self._samples.clear()
        self._previous_time = None
        self._previous_vector = None
        self._next_time = None

    def push(self, timestamp_ms: int | float, features) -> np.ndarray | None:
        if features is None:
            self.reset()
            return None
        vector = np.asarray(features, dtype=np.float32)
        if (not math.isfinite(timestamp_ms) or timestamp_ms < 0
                or vector.shape != (44,) or not np.isfinite(vector).all()):
            self.reset()
            raise ValueError("Expected a finite timestamp and 44 finite features.")
        if self._previous_time is not None:
            gap = timestamp_ms - self._previous_time
            if gap <= 0:
                self.reset()
                raise ValueError("Timestamps must be strictly increasing.")
            if gap > self._max_gap_ms:
                self.reset()

        added = False
        if self._previous_time is None:
            self._samples.append(vector.copy())
            self._next_time = timestamp_ms + self._step_ms
            added = True
        else:
            while self._next_time <= timestamp_ms + 1e-9:
                fraction = (self._next_time - self._previous_time) / (timestamp_ms - self._previous_time)
                sample = self._previous_vector + fraction * (vector - self._previous_vector)
                self._samples.append(sample.astype(np.float32))
                self._next_time += self._step_ms
                added = True
        self._previous_time = timestamp_ms
        self._previous_vector = vector.copy()
        if added and self.size == self.length:
            return np.stack(self._samples)
        return None
