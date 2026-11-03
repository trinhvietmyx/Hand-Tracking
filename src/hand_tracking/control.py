"""TODO: Confidence gate, cooldown and a single OS action adapter.

SWIPE_LEFT -> right arrow; SWIPE_RIGHT -> left arrow;
SWIPE_UP -> positive scroll; SWIPE_DOWN -> negative scroll.
Start disabled, keep fail-safe, clear pending gestures on pause/hand loss.
Re-arm only after cooldown AND stable background. No OS calls exist yet.
"""
