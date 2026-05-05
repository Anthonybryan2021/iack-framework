import unittest
from src.metrics import compute_iack_metrics


class TestMetricsPrototype(unittest.TestCase):
    def test_compute_iack_metrics_outputs_expected_keys(self):
        data = compute_iack_metrics()
        self.assertIsInstance(data, dict)
        self.assertIn("integrity", data)
        self.assertIn("availability", data)
        self.assertIn("confidentiality_proxy", data)
        self.assertIn("windowed_efficiency", data)

    def test_metric_values_are_numeric(self):
        data = compute_iack_metrics()
        self.assertIsInstance(data["integrity"], (int, float))
        self.assertIsInstance(data["availability"], (int, float))
        self.assertIsInstance(data["confidentiality_proxy"], (int, float))
        self.assertIsInstance(data["windowed_efficiency"], (int, float))

    def test_invalid_total_events_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(total_events=0)

    def test_invalid_window_size_raises_error(self):
        with self.assertRaises(ValueError):
            compute_iack_metrics(window_size=0)

    def test_placeholder_metrics_remain_one(self):
        data = compute_iack_metrics()
        self.assertEqual(data["integrity"], 1.0)
        self.assertEqual(data["availability"], 1.0)
        self.assertEqual(data["confidentiality_proxy"], 1.0)

    def test_windowed_efficiency_reflects_inputs(self):
        data = compute_iack_metrics(total_events=3, window_size=5)
        self.assertAlmostEqual(data["windowed_efficiency"], 0.6)