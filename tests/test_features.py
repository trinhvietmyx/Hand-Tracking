"""Prevent lost global motion, distorted image axes and stale temporal samples."""

import unittest

import numpy as np

from hand_tracking import features


def hand_points():
    points = np.tile([0.25, 0.5], (21, 1)).astype(np.float32)
    points[5] = [0.375, 0.5]
    points[9] = [0.25, 2 / 3]
    points[13] = [0.125, 0.5]
    points[17] = [0.25, 1 / 3]
    points[8] = [0.5, 0.5]
    return points


class FeatureTests(unittest.TestCase):
    def setUp(self):
        self.extract = getattr(features, "extract_features", None)
        self.assertTrue(callable(self.extract), "extract_features is not implemented")

    def test_normalizes_both_axes_in_the_same_image_scale(self):
        result = self.extract(hand_points(), frame_size=(640, 480))
        self.assertEqual(result.shape, (44,))
        self.assertEqual(result.dtype, np.dtype("float32"))
        np.testing.assert_allclose(result[:2], [0, 0])
        np.testing.assert_allclose(result[10:12], [1, 0], atol=1e-6)
        np.testing.assert_allclose(result[18:20], [0, 1], atol=1e-6)
        np.testing.assert_allclose(result[-2:], [0.25, 0.375])

    def test_translation_preserves_local_shape_but_changes_global_wrist(self):
        original = self.extract(hand_points(), frame_size=(640, 480))
        moved = self.extract(hand_points() + [0.125, 0], frame_size=(640, 480))
        np.testing.assert_allclose(moved[:42], original[:42], atol=1e-6)
        np.testing.assert_allclose(moved[-2:] - original[-2:], [0.125, 0])

    def test_hand_size_change_preserves_local_shape(self):
        points = hand_points()
        scaled = points[0] + (points - points[0]) * 1.5
        original = self.extract(points, frame_size=(640, 480))
        result = self.extract(scaled, frame_size=(640, 480))
        np.testing.assert_allclose(result, original, atol=1e-6)

    def test_rejects_invalid_or_degenerate_landmarks(self):
        invalid = [np.zeros((20, 2)), np.zeros((21, 2)), np.full((21, 2), np.nan)]
        for points in invalid:
            with self.subTest(shape=points.shape), self.assertRaises(ValueError):
                self.extract(points, frame_size=(640, 480))
        with self.assertRaises(ValueError):
            self.extract(hand_points(), frame_size=(640, 0))


class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.buffer_type = getattr(features, "SequenceBuffer", None)
        self.assertTrue(callable(self.buffer_type), "SequenceBuffer is not implemented")

    def test_interpolates_only_available_observations_onto_50ms_grid(self):
        buffer = self.buffer_type(length=3, sample_rate_hz=20)
        self.assertIsNone(buffer.push(0, np.zeros(44)))
        self.assertIsNone(buffer.push(40, np.full(44, 4)))
        self.assertIsNone(buffer.push(80, np.full(44, 8)))
        sequence = buffer.push(120, np.full(44, 12))
        self.assertEqual(sequence.shape, (3, 44))
        np.testing.assert_allclose(sequence[:, 0], [0, 5, 10])

    def test_fast_camera_does_not_duplicate_temporal_samples(self):
        buffer = self.buffer_type(length=3, sample_rate_hz=20)
        for timestamp in range(0, 50, 10):
            self.assertIsNone(buffer.push(timestamp, np.ones(44)))
        self.assertEqual(buffer.size, 1)
        buffer.push(50, np.ones(44))
        self.assertEqual(buffer.size, 2)

    def test_long_gap_starts_a_fresh_sequence(self):
        buffer = self.buffer_type(length=3)
        buffer.push(0, np.zeros(44))
        buffer.push(50, np.ones(44))
        self.assertIsNone(buffer.push(200, np.full(44, 2)))
        self.assertEqual(buffer.size, 1)

    def test_missing_hand_clears_previous_samples(self):
        buffer = self.buffer_type(length=3)
        buffer.push(0, np.zeros(44))
        buffer.push(50, np.ones(44))
        buffer.push(100, None)
        self.assertEqual(buffer.size, 0)
        self.assertIsNone(buffer.push(150, np.ones(44)))
        self.assertEqual(buffer.size, 1)

    def test_invalid_or_out_of_order_input_cannot_leave_a_ready_sequence(self):
        for timestamp, vector in ((0, np.ones(44)), (50, np.full(44, np.nan)), (50, np.ones(43))):
            buffer = self.buffer_type(length=1)
            buffer.push(0, np.zeros(44))
            with self.subTest(timestamp=timestamp, shape=vector.shape), self.assertRaises(ValueError):
                buffer.push(timestamp, vector)
            self.assertEqual(buffer.size, 0)


if __name__ == "__main__":
    unittest.main()
