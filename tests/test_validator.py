import pytest

from iack.validators.assessment_validator import validate_assessment


def make_valid_assessment():
    return {
        "assessment_id": "IACK-TEST-0001",
        "system_name": "Test System",
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


def test_validate_assessment_accepts_valid_input():
    data = make_valid_assessment()
    result = validate_assessment(data)
    assert result == []


def test_validate_assessment_rejects_weights_not_equal_to_one():
    data = make_valid_assessment()
    data["metrics"][0]["weight"] = 0.5
    result = validate_assessment(data)
    assert result
    assert any("weight" in err.lower() for err in result)


def test_validate_assessment_rejects_missing_evidence():
    data = make_valid_assessment()
    data["metrics"][2]["evidence"] = []
    result = validate_assessment(data)
    assert result
    assert any("evidence" in err.lower() for err in result)


def test_validate_assessment_rejects_missing_top_level_field():
    data = make_valid_assessment()
    del data["system_name"]
    result = validate_assessment(data)
    assert "Missing top-level field: system_name" in result


def test_validate_assessment_rejects_empty_metrics_list():
    data = make_valid_assessment()
    data["metrics"] = []
    result = validate_assessment(data)
    assert "metrics must be a non-empty list" in result


def test_validate_assessment_rejects_missing_metric_field():
    data = make_valid_assessment()
    del data["metrics"][0]["confidence_rule"]
    result = validate_assessment(data)
    assert "Metric #1 missing field: confidence_rule" in result


def test_validate_assessment_rejects_non_numeric_weight():
    data = make_valid_assessment()
    data["metrics"][0]["weight"] = "heavy"
    result = validate_assessment(data)
    assert "CONF-001 weight must be numeric" in result


def test_validate_assessment_rejects_threshold_out_of_range():
    data = make_valid_assessment()
    data["metrics"][1]["threshold"] = 1.5
    result = validate_assessment(data)
    assert "AUTH-001 threshold must be between 0 and 1" in result


def test_validate_assessment_rejects_score_out_of_range():
    data = make_valid_assessment()
    data["metrics"][2]["score"] = -0.1
    result = validate_assessment(data)
    assert "INTEG-001 score must be between 0 and 1" in result


def test_validate_assessment_rejects_non_list_evidence():
    data = make_valid_assessment()
    data["metrics"][1]["evidence"] = "logs"
    result = validate_assessment(data)
    assert "AUTH-001 evidence must be a list" in result

import json
from iack.validators.assessment_validator import main


def test_validator_main_returns_1_when_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["validator"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Usage: python -m iack.validators.assessment_validator <input_json>" in captured.out


def test_validator_main_returns_1_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["validator", "does_not_exist.json"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Input file not found: does_not_exist.json" in captured.out


def test_validator_main_returns_0_for_valid_file(monkeypatch, capsys, tmp_path):
    data = make_valid_assessment()
    input_file = tmp_path / "assessment.json"
    input_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["validator", str(input_file)])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 0
    assert "Validation passed." in captured.out


def test_validator_main_returns_1_for_invalid_file(monkeypatch, capsys, tmp_path):
    data = make_valid_assessment()
    data["metrics"][0]["weight"] = 0.5
    input_file = tmp_path / "assessment_bad.json"
    input_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["validator", str(input_file)])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Validation failed:" in captured.out
    assert "Metric weights must sum to 1.00" in captured.out
