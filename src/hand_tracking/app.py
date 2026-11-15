"""Camera, landmark and feature preview with optional gesture prediction."""

from contextlib import nullcontext
from queue import SimpleQueue
from threading import Event
from time import perf_counter

import cv2
import numpy as np

from .camera import Camera
from .config import ProjectConfig
from .features import SequenceBuffer, extract_features
from .landmarks import HandTracker


HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
)


def draw_preview(image, observation, state, buffer_size, config, fps,
                 footer="PREVIEW ONLY | Q / ESC / close window: exit"):
    if observation.landmarks_xy is not None:
        height, width = image.shape[:2]
        points = observation.landmarks_xy * [width, height]
        points = np.clip(points, [0, 0], [width - 1, height - 1]).astype(int)
        for start, end in HAND_CONNECTIONS:
            cv2.line(image, tuple(points[start]), tuple(points[end]), (70, 200, 100), 2)
        for point in points:
            cv2.circle(image, tuple(point), 3, (70, 220, 240), -1)
    cv2.rectangle(image, (0, 0), (image.shape[1], 88), (25, 25, 25), -1)
    lines = (
        f"Hand: {state} | FPS: {fps:.1f} | Mirror: {config.mirror}",
        f"Features: 44 | Samples: {buffer_size}/{config.sequence_length} @ {config.sample_rate_hz} Hz",
        footer,
    )
    for index, text in enumerate(lines):
        cv2.putText(image, text, (10, 23 + index * 26), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 240, 240), 1, cv2.LINE_AA)


def poll_key(window: str) -> int:
    """Return a key, treating a closed native window as Escape."""
    key = cv2.waitKey(1) & 0xFF
    if key in (27, ord("q")):
        return key
    try:
        if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
            return 27
    except cv2.error:
        return 27
    return key


def run_preview(
    config: ProjectConfig,
    headless: bool = False,
    max_frames: int | None = None,
    *,
    predict: bool = False,
) -> dict:
    """Preview frames in memory and dispatch confirmed gestures when enabled."""
    if max_frames is not None and max_frames < 1:
        raise ValueError("max_frames must be positive.")
    if headless and max_frames is None:
        raise ValueError("Headless preview requires max_frames to avoid an endless run.")
    footer = "PREVIEW ONLY | Q / ESC / close window: exit"
    hotkeys = nullcontext()
    toggle_requests = SimpleQueue()
    stop_requested = Event()
    control_enabled = False
    control_status = "OFF"

    if predict:
        from .control import GestureGate, send_gesture_action
        from .model import load_gesture_model, predict_gesture

        model, _ = load_gesture_model(config)
        gate = GestureGate(config)
        last_confirmed = "-"
        confirmed_count = 0
        footer = "Control OFF | Collecting samples..."

        if not headless:
            from pynput.keyboard import GlobalHotKeys
            from pyautogui import FailSafeException

            hotkeys = GlobalHotKeys({
                f"<{config.toggle_key}>": lambda: toggle_requests.put(None),
                f"<{config.stop_key}>": stop_requested.set,
            })

    buffer = SequenceBuffer(config.sequence_length, config.sample_rate_hz)
    frames = valid_frames = ready_count = 0
    state = "starting"
    window = "Hand-Tracking | camera and features"
    window_created = False
    started = perf_counter()
    try:
        with hotkeys, HandTracker(config.landmarker_path) as tracker, Camera(config) as camera:
            started = perf_counter()
            if not headless:
                cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)
                window_created = True
            while max_frames is None or frames < max_frames:
                frame = camera.read()
                if stop_requested.is_set():
                    break

                while not toggle_requests.empty():
                    toggle_requests.get_nowait()
                    control_enabled = not control_enabled
                    control_status = "ON" if control_enabled else "OFF"
                    buffer.reset()
                    gate.reset()
                    last_confirmed = "-"
                    footer = f"Control {control_status} | Collecting samples..."

                observation = tracker.detect(frame.image, frame.timestamp_ms)
                vector = None
                state = observation.reason or "one_hand"
                if observation.landmarks_xy is not None:
                    height, width = frame.image.shape[:2]
                    try:
                        vector = extract_features(observation.landmarks_xy, (width, height))
                    except ValueError:
                        state = "invalid_landmarks"
                sequence = buffer.push(frame.timestamp_ms, vector)
                if predict:
                    if sequence is not None:
                        label, confidence = predict_gesture(model, sequence)

                        if control_enabled:
                            confirmed = gate.update(
                                label, confidence, frame.timestamp_ms
                            )
                            if (
                                confirmed is not None
                                and not stop_requested.is_set()
                                and toggle_requests.empty()
                            ):
                                try:
                                    action = send_gesture_action(
                                        confirmed, config.scroll_steps
                                    )
                                except FailSafeException:
                                    print("PyAutoGUI fail-safe triggered. Stopping.")
                                    break

                                last_confirmed = action
                                confirmed_count += 1

                        footer = (
                            f"Control {control_status} | {label.name} {confidence:.1%} | "
                            f"Confirmed: {last_confirmed} ({confirmed_count})"
                        )
                    elif buffer.size < config.sequence_length:
                        gate.update(None, 0.0, frame.timestamp_ms)
                        footer = (
                            f"Control {control_status} | Collecting samples... | "
                            f"Confirmed: {confirmed_count}"
                        )
                frames += 1
                valid_frames += int(vector is not None)
                ready_count += int(sequence is not None)
                if not headless:
                    fps = frames / max(perf_counter() - started, 1e-9)
                    draw_preview(
                        frame.image, observation, state, buffer.size, config, fps,
                        footer=footer,
                    )
                    cv2.imshow(window, frame.image)
                    if poll_key(window) in (27, ord("q")):
                        break
    finally:
        if window_created:
            cv2.destroyAllWindows()
    elapsed = max(perf_counter() - started, 1e-9)
    return {
        "mode": "preview",
        "frames": frames,
        "valid_hand_frames": valid_frames,
        "average_processing_fps": round(frames / elapsed, 2),
        "buffer_size": buffer.size,
        "sequences_ready": ready_count,
        "last_sequence_shape": [config.sequence_length, 44] if buffer.size == config.sequence_length else None,
        "last_state": state,
        "control_enabled": control_enabled,
        "recording_enabled": False,
    }
