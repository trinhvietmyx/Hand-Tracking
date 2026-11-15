"""Verify the slide navigation keys without sending desktop input."""

import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from hand_tracking.control import send_gesture_action
from hand_tracking.labels import Gesture


class SlideNavigationTests(unittest.TestCase):
    def test_horizontal_swipes_send_matching_arrow_keys(self):
        for gesture, key, action in (
            (Gesture.SWIPE_LEFT, "left", "PREV SLIDE"),
            (Gesture.SWIPE_RIGHT, "right", "NEXT SLIDE"),
        ):
            with self.subTest(gesture=gesture):
                press = Mock()
                with patch.dict(sys.modules, {"pyautogui": SimpleNamespace(press=press)}):
                    result = send_gesture_action(gesture, scroll_steps=3)

                press.assert_called_once_with(key)
                self.assertEqual(result, action)
