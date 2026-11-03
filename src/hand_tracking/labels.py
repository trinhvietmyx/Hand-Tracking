"""Shared class IDs for recordings, model logits and runtime decisions."""

from enum import IntEnum


class Gesture(IntEnum):
    BACKGROUND = 0
    SWIPE_LEFT = 1
    SWIPE_RIGHT = 2
    SWIPE_UP = 3
    SWIPE_DOWN = 4


CLASS_NAMES = tuple(gesture.name for gesture in Gesture)
