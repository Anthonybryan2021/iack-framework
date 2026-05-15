import unittest
from src.metrics import compute_iack_metrics

import unittest
from src.metrics import compute_iack_metrics


class TestMetricsPrototype(unittest.TestCase):
    def test_compute_iack_metrics_outputs_expected_keys(self):
        data = compute_iack_metrics()
        self.assertIsInstance(data, dict)
        self.assertEqual(
            set(data.keys()),
            {
                "integrity",
                "availability",
                "confidentiality_proxy",
                "windowed_efficiency",
            },
        )

    def test_metric_values_are_numeric(self):
        data = compute_iack_metrics()
        for value in data.values():
            self.assertIsInstance(value, (int, float))

    def test_all_metric_values_are_bounded_between_zero_and_one(self):
        data = compute_iack_metrics(total_events=3, window_size=5)
        for value in data.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_invalid_total_events_zero_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(total_events=0)

    def test_invalid_window_size_zero_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(window_size=0)

    def test_negative_total_events_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(total_events=-1)

    def test_negative_window_size_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(window_size=-1)

    def test_placeholder_metrics_remain_one(self):
        data = compute_iack_metrics()
        self.assertEqual(data["availability"], 1.0)
        self.assertEqual(data["confidentiality_proxy"], 1.0)

    def test_integrity_reflects_total_events(self):
        data = compute_iack_metrics(total_events=3, window_size=5)
        self.assertAlmostEqual(data["integrity"], 0.3)

    def test_windowed_efficiency_reflects_inputs(self):
        data = compute_iack_metrics(total_events=3, window_size=5)
        self.assertAlmostEqual(data["windowed_efficiency"], 0.6)

    def test_integrity_saturates_at_one_at_boundary(self):
        data = compute_iack_metrics(total_events=10, window_size=20)
        self.assertEqual(data["integrity"], 1.0)

    def test_integrity_remains_one_after_boundary(self):
        data = compute_iack_metrics(total_events=11, window_size=20)
        self.assertEqual(data["integrity"], 1.0)

    def test_windowed_efficiency_saturates_at_one_when_events_equal_window(self):
        data = compute_iack_metrics(total_events=5, window_size=5)
        self.assertEqual(data["windowed_efficiency"], 1.0)

    def test_windowed_efficiency_caps_at_one_when_events_exceed_window(self):
        data = compute_iack_metrics(total_events=6, window_size=5)
        self.assertEqual(data["windowed_efficiency"], 1.0)

    def test_same_inputs_produce_same_output(self):
        result_one = compute_iack_metrics(total_events=3, window_size=5)
        result_two = compute_iack_metrics(total_events=3, window_size=5)
        self.assertEqual(result_one, result_two)
