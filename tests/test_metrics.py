import unittest
from src.metrics import compute_iack_metrics


class TestMetricsTypeValidation(unittest.TestCase):
    def test_none_total_events_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events=None, window_size=1)

    def test_none_window_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events=1, window_size=None)

    def test_string_total_events_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events="3", window_size=5)

    def test_string_window_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events=3, window_size="5")

    def test_bool_total_events_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events=True, window_size=5)

    def test_bool_window_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_iack_metrics(total_events=1, window_size=False)