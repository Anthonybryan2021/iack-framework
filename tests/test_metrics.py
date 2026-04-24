import ast
import subprocess
import sys
import unittest
from pathlib import Path


class TestMetricsPrototype(unittest.TestCase):
    def test_metrics_script_outputs_expected_keys(self):
        repo_root = Path(__file__).resolve().parents[1]
        script = repo_root / "src" / "metrics.py"

        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            check=True,
        )

        output = result.stdout.strip()
        self.assertTrue(output, "metrics.py did not print any output")

        data = ast.literal_eval(output)

        self.assertIsInstance(data, dict)
        self.assertIn("integrity", data)
        self.assertIn("availability", data)
        self.assertIn("confidentiality_proxy", data)
        self.assertIn("windowed_efficiency", data)

    def test_metric_values_are_numeric(self):
        repo_root = Path(__file__).resolve().parents[1]
        script = repo_root / "src" / "metrics.py"

        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            check=True,
        )

        data = ast.literal_eval(result.stdout.strip())

        self.assertIsInstance(data["integrity"], (int, float))
        self.assertIsInstance(data["availability"], (int, float))
        self.assertIsInstance(data["confidentiality_proxy"], (int, float))
        self.assertIsInstance(data["windowed_efficiency"], (int, float))
