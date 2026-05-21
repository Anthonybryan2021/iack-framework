import json
import pytest

from iack.metrics.model import confidence_from_evidence_count, main, score_assessment


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


def test_confidence_from_evidence_count_high():
    assert confidence_from_evidence_count(3) == "high"
    assert confidence_from_evidence_count(5) == "high"


def test_confidence_from_evidence_count_medium():
    assert confidence_from_evidence_count(2) == "medium"


def test_confidence_from_evidence_count_low():
    assert confidence_from_evidence_count(1) == "low"
    assert confidence_from_evidence_count(0) == "low"


def test_score_assessment_returns_expected_weighted_score():
    data = make_valid_assessment()
    result = score_assessment(data)

    assert result["assessment_id"] == "IACK-TEST-0001"
    assert round(result["overall_weighted_score"], 3) == 0.754


def test_score_assessment_returns_expected_pass_fail_counts():
    data = make_valid_assessment()
    result = score_assessment(data)

    assert result["metrics_passed"] == 2
    assert result["metrics_failed"] == 1
    assert len(result["metric_results"]) == 3


def test_score_assessment_marks_integrity_metric_as_failed():
    data = make_valid_assessment()
    result = score_assessment(data)

    integrity_metric = next(
        metric for metric in result["metric_results"]
        if metric["metric_id"] == "INTEG-001"
    )

    assert integrity_metric["domain"] == "integrity"
    assert integrity_metric["passed"] is False
    assert integrity_metric["evidence_count"] == 1


def test_score_assessment_raises_value_error_for_non_numeric_score():
    data = make_valid_assessment()
    data["metrics"][0]["score"] = "not-a-number"

    with pytest.raises(ValueError):
        score_assessment(data)


def test_model_main_returns_1_when_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["model"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Usage: python -m iack.metrics.model <input_json>" in captured.out


def test_model_main_returns_1_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["model", "does_not_exist.json"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Input file not found: does_not_exist.json" in captured.out


def test_model_main_returns_0_and_prints_json(monkeypatch, capsys, tmp_path):
    data = make_valid_assessment()
    input_file = tmp_path / "assessment.json"
    input_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["model", str(input_file)])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 0
    parsed = json.loads(captured.out)
    assert parsed["assessment_id"] == "IACK-TEST-0001"
    assert parsed["metrics_passed"] == 2
    assert parsed["metrics_failed"] == 1
