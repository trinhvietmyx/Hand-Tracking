import sys

from .config import ProjectConfig
from .labels import Gesture


class GestureGate:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.reset()

    def reset(self) -> None:
        self._clear_candidate()
        self._blocked_until_ms = None
        self._background_since_ms = None

    def _clear_candidate(self) -> None:
        self._candidate = None
        self._candidate_since_ms = 0.0
        self._candidate_count = 0

    def update(
        self, label: Gesture | None, confidence: float, timestamp_ms: float
    ) -> Gesture | None:
        if label is None or not (self.config.confidence_threshold <= confidence <= 1.0):
            self._clear_candidate()
            self._background_since_ms = None
            return None

        if self._blocked_until_ms is not None:
            if label != Gesture.BACKGROUND:
                self._background_since_ms = None
                return None

            if self._background_since_ms is None:
                self._background_since_ms = timestamp_ms

            background_ms = timestamp_ms - self._background_since_ms
            if (
                timestamp_ms >= self._blocked_until_ms
                and background_ms >= self.config.background_ms
            ):
                self._blocked_until_ms = None
                self._background_since_ms = None
            return None

        if label == Gesture.BACKGROUND:
            self._clear_candidate()
            return None

        if label != self._candidate:
            self._candidate = label
            self._candidate_since_ms = timestamp_ms
            self._candidate_count = 0

        self._candidate_count += 1
        stable_ms = timestamp_ms - self._candidate_since_ms
        if (
            self._candidate_count >= self.config.min_predictions
            and stable_ms >= self.config.stable_ms
        ):
            self._blocked_until_ms = timestamp_ms + self.config.cooldown_ms
            self._clear_candidate()
            return label

        return None


def send_gesture_action(gesture: Gesture, scroll_steps: int) -> str:
    import pyautogui

    if gesture == Gesture.SWIPE_LEFT:
        pyautogui.press("left")
        return "PREV SLIDE"

    if gesture == Gesture.SWIPE_RIGHT:
        pyautogui.press("right")
        return "NEXT SLIDE"

    wheel_delta = scroll_steps * 120 if sys.platform == "win32" else scroll_steps

    if gesture == Gesture.SWIPE_UP:
        pyautogui.scroll(wheel_delta)
        return "SCROLL UP"

    if gesture == Gesture.SWIPE_DOWN:
        pyautogui.scroll(-wheel_delta)
        return "SCROLL DOWN"

    raise ValueError(f"No action for {gesture.name}")
