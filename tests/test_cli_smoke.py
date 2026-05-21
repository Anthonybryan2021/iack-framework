import json
import subprocess
import sys


def make_valid_assessment():
    return {
        "assessment_id": "IACK-SMOKE-0001",
        "system_name": "CLI Smoke System",
        "assessment_date": "2026-05-21",
        "metrics": [
            {
                "metric_id": "CONF-001",
                "metric_name": "Confidentiality Control Strength",
                "domain": "confidentiality",
                "score": 0.82,
                "weight": 0.4,
                "threshold": 0.7,
                "confidence": "high",
                "confidence_rule": "evidence_count >= 3",
                "evidence": ["policy", "control test", "review"]
            },
            {
                "metric_id": "AUTH-001",
                "metric_name": "Authenticity Assurance",
                "domain": "authenticity",
                "score": 0.74,
                "weight": 0.3,
                "threshold": 0.65,
                "confidence": "medium",
                "confidence_rule": "evidence_count >= 2",
                "evidence": ["logs", "config"]
            },
            {
                "metric_id": "INTEG-001",
                "metric_name": "Integrity Verification Coverage",
                "domain": "integrity",
                "score": 0.68,
                "weight": 0.3,
                "threshold": 0.75,
                "confidence": "low",
                "confidence_rule": "evidence_count >= 1",
                "evidence": ["hash-check"]
            }
        ]
    }


def test_cli_smoke_pipeline(tmp_path):
    input_file = tmp_path / "assessment.json"
    input_file.write_text(json.dumps(make_valid_assessment()), encoding="utf-8")

    result_validator = subprocess.run(
        [sys.executable, "-m", "iack.validators.assessment_validator", str(input_file)],
        capture_output=True,
        text=True,
        cwd=tmp_path
    )
    assert result_validator.returncode == 0
    assert "Validation passed." in result_validator.stdout

    result_model = subprocess.run(
        [sys.executable, "-m", "iack.metrics.model", str(input_file)],
        capture_output=True,
        text=True,
        cwd=tmp_path
    )
    assert result_model.returncode == 0
    assert '"assessment_id": "IACK-SMOKE-0001"' in result_model.stdout

    result_mapping = subprocess.run(
        [sys.executable, "-m", "iack.mappings.csf_mapping", str(input_file)],
        capture_output=True,
        text=True,
        cwd=tmp_path
    )
    assert result_mapping.returncode == 0
    assert "assessment_result_mapped.json" in result_mapping.stdout

    result_report = subprocess.run(
        [sys.executable, "-m", "iack.outputs.report_writer", str(input_file)],
        capture_output=True,
        text=True,
        cwd=tmp_path
    )
    assert result_report.returncode == 0
    assert "assessment_result.json" in result_report.stdout
    assert (tmp_path / "data" / "output" / "assessment_result.json").exists()
    assert (tmp_path / "data" / "output" / "assessment_result.csv").exists()
    assert (tmp_path / "data" / "output" / "assessment_result.md").exists()
