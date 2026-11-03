"""Manual, labelled recording with countdown, quality rejection and resumption."""

import math
from time import perf_counter

import cv2
import numpy as np

from .app import draw_preview, poll_key
from .camera import Camera, CameraFrame
from .config import ProjectConfig
from .dataset import DatasetStore, RecordedClip
from .features import SequenceBuffer, extract_features
from .labels import Gesture
from .landmarks import HandObservation, HandTracker


class ClipRejected(ValueError):
    """Discard this entire attempt; start a new one rather than stitching gaps."""


class ClipAttempt:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.buffer = SequenceBuffer(config.sequence_length, config.sample_rate_hz)
        self._frames, self._timestamps, self._landmarks = [], [], []
        self._finished = False

    def push(self, frame: CameraFrame, observation: HandObservation) -> RecordedClip | None:
        if self._finished:
            raise ClipRejected("This attempt ended; start a new recording.")
        reason = observation.reason
        if observation.hand_count != 1 or observation.landmarks_xy is None:
            reason = reason or "invalid_hand"
        elif self._timestamps and not 0 < frame.timestamp_ms - self._timestamps[-1] <= 100:
            reason = "tracking_gap_or_timestamp_error"
        if reason:
            self._finished = True
            raise ClipRejected(reason)
        try:
            height, width = frame.image.shape[:2]
            vector = extract_features(observation.landmarks_xy, (width, height))
            sequence = self.buffer.push(frame.timestamp_ms, vector)
        except ValueError as error:
            self._finished = True
            raise ClipRejected(str(error)) from error
        self._frames.append(frame.image.copy())
        self._timestamps.append(frame.timestamp_ms)
        self._landmarks.append(observation.landmarks_xy.copy())
        if sequence is None:
            return None
        self._finished = True
        times = np.asarray(self._timestamps, dtype=np.float64) - self._timestamps[0]
        step = 1000 / self.config.sample_rate_hz
        last_grid_index = math.floor(times[-1] / step + 1e-9)
        sample_times = (np.arange(self.config.sequence_length)
                        + last_grid_index - self.config.sequence_length + 1) * step
        return RecordedClip(sequence, self._frames, times, np.stack(self._landmarks), sample_times)


_INSTRUCTIONS = {
    Gesture.BACKGROUND: "Rest hand or move slowly; do not swipe",
    Gesture.SWIPE_LEFT: "One swipe RIGHT -> LEFT in mirrored view",
    Gesture.SWIPE_RIGHT: "One swipe LEFT -> RIGHT in mirrored view",
    Gesture.SWIPE_UP: "One swipe BOTTOM -> TOP",
    Gesture.SWIPE_DOWN: "One swipe TOP -> BOTTOM",
}


def collect_clips(config: ProjectConfig, session_id: str, split: str, count: int,
                  labels=None, countdown_seconds: float = 2, max_frames: int | None = None) -> dict:
    """SPACE starts one attempt; Q/Escape/close aborts only the unfinished attempt.

    count is a target per selected label in this session, including existing
    clips. A successful attempt is saved before another one can be started.
    """
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer.")
    if not math.isfinite(countdown_seconds) or countdown_seconds < 0:
        raise ValueError("countdown_seconds must be finite and non-negative.")
    if max_frames is not None and max_frames < 1:
        raise ValueError("max_frames must be positive.")
    labels = list(Gesture) if labels is None else [Gesture(label) for label in labels]
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("Select at least one label, without duplicates.")
    store = DatasetStore(config, session_id, split)
    counts = store.counts()
    saved = rejected = frames = 0
    completed = all(counts[label.name] >= count for label in labels)
    phase, message = "waiting", "SPACE to start; Q / ESC to exit"
    countdown_start = 0
    attempt = None
    window, created = "Hand-Tracking | labelled collection", False
    try:
        if not completed:
            with HandTracker(config.landmarker_path) as tracker, Camera(config) as camera:
                cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)
                created = True
                started = perf_counter()
                while max_frames is None or frames < max_frames:
                    label = next(label for label in labels if counts[label.name] < count)
                    frame = camera.read()
                    observation = tracker.detect(frame.image, frame.timestamp_ms)
                    frames += 1
                    state = observation.reason or "one_hand"
                    if phase == "countdown":
                        remaining = countdown_seconds - (frame.timestamp_ms - countdown_start) / 1000
                        message = f"GET READY: {max(0, math.ceil(remaining))}"
                        if remaining <= 0:
                            attempt, phase = ClipAttempt(config), "recording"
                    if phase == "recording":
                        message = "RECORDING - perform the gesture now"
                        try:
                            clip = attempt.push(frame, observation)
                        except ClipRejected as error:
                            rejected += 1
                            phase, attempt = "waiting", None
                            message = f"RETRY: {error} | SPACE when ready"
                        else:
                            if clip is not None:
                                store.save(clip, label)
                                counts[label.name] += 1
                                saved += 1
                                phase, attempt = "waiting", None
                                message = f"SAVED {label.name} {counts[label.name]}/{count} | SPACE next"
                                completed = all(counts[item.name] >= count for item in labels)
                    fps = frames / max(perf_counter() - started, 1e-9)
                    samples = attempt.buffer.size if attempt is not None else 0
                    draw_preview(frame.image, observation, state, samples, config, fps,
                                 footer=f"{label.name} {counts[label.name]}/{count} | {split} | {session_id}")
                    height, width = frame.image.shape[:2]
                    cv2.rectangle(frame.image, (0, max(0, height - 88)), (width, height), (25, 25, 25), -1)
                    cv2.putText(frame.image, message, (10, max(18, height - 56)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (80, 230, 230), 1, cv2.LINE_AA)
                    cv2.putText(frame.image, _INSTRUCTIONS[label], (10, max(38, height - 25)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 235, 235), 1, cv2.LINE_AA)
                    cv2.imshow(window, frame.image)
                    if completed:
                        break
                    key = poll_key(window)
                    if key in (27, ord("q")):
                        break
                    if key == 32 and phase == "waiting":
                        if observation.landmarks_xy is None or observation.hand_count != 1:
                            message = "Keep exactly one hand visible, then press SPACE"
                        else:
                            phase, countdown_start = "countdown", frame.timestamp_ms
    finally:
        if created:
            cv2.destroyAllWindows()
    return {"mode": "collect", "session_id": session_id, "split": split,
            "target_per_label": count, "counts": counts, "saved_this_run": saved,
            "rejected_attempts": rejected, "completed": completed, "aborted": not completed,
            "control_enabled": False}
