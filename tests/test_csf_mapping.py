from iack.mappings.csf_mapping import apply_csf_mapping


def make_scored_result():
    return {
        "assessment_id": "IACK-TEST-0001",
        "system_name": "Test System",
        "assessment_date": "2026-05-21",
        "overall_weighted_score": 0.754,
        "metrics_passed": 2,
        "metrics_failed": 1,
        "metric_results": [
            {
                "metric_id": "CONF-001",
                "metric_name": "Confidentiality Control Strength",
                "domain": "confidentiality",
                "score": 0.82,
                "weight": 0.4,
                "threshold": 0.7,
                "passed": True,
                "confidence": "high",
                "evidence_count": 3
            },
            {
                "metric_id": "AUTH-001",
                "metric_name": "Authenticity Assurance",
                "domain": "authenticity",
                "score": 0.74,
                "weight": 0.3,
                "threshold": 0.65,
                "passed": True,
                "confidence": "medium",
                "evidence_count": 2
            },
            {
                "metric_id": "INTEG-001",
                "metric_name": "Integrity Verification Coverage",
                "domain": "integrity",
                "score": 0.68,
                "weight": 0.3,
                "threshold": 0.75,
                "passed": False,
                "confidence": "low",
                "evidence_count": 1
            }
        ]
    }


def test_apply_csf_mapping_returns_metric_results():
    result = apply_csf_mapping(make_scored_result())

    assert result["assessment_id"] == "IACK-TEST-0001"
    assert "metric_results" in result
    assert len(result["metric_results"]) == 3


def test_apply_csf_mapping_applies_expected_codes():
    result = apply_csf_mapping(make_scored_result())

    confidentiality_metric = next(
        metric for metric in result["metric_results"]
        if metric["domain"] == "confidentiality"
    )
    integrity_metric = next(
        metric for metric in result["metric_results"]
        if metric["domain"] == "integrity"
    )

    assert confidentiality_metric["csf_function"] == "Protect"
    assert confidentiality_metric["csf_code"] == "PR"
    assert integrity_metric["csf_function"] == "Detect"
    assert integrity_metric["csf_code"] == "DE"


def test_apply_csf_mapping_preserves_original_metric_fields():
    result = apply_csf_mapping(make_scored_result())

    auth_metric = next(
        metric for metric in result["metric_results"]
        if metric["metric_id"] == "AUTH-001"
    )

    assert auth_metric["metric_name"] == "Authenticity Assurance"
    assert auth_metric["passed"] is True
    assert auth_metric["confidence"] == "medium"


def test_apply_csf_mapping_uses_default_mapping_for_unknown_domain():
    result = make_scored_result()
    result["metric_results"].append(
        {
            "metric_id": "UNK-001",
            "metric_name": "Unknown Domain Metric",
            "domain": "resilience_ops",
            "score": 0.9,
            "weight": 0.1,
            "threshold": 0.7,
            "passed": True,
            "confidence": "high",
            "evidence_count": 4
        }
    )

    mapped = apply_csf_mapping(result)
    unknown_metric = next(
        metric for metric in mapped["metric_results"]
        if metric["metric_id"] == "UNK-001"
    )

    assert unknown_metric["csf_function"] == "Identify"
    assert unknown_metric["csf_code"] == "ID"
    assert "Default mapping used" in unknown_metric["rationale"]

import json
from iack.mappings.csf_mapping import main


def make_input_assessment():
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


def test_csf_mapping_main_returns_1_when_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["csf_mapping"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Usage: python -m iack.mappings.csf_mapping <input_json>" in captured.out


def test_csf_mapping_main_returns_1_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["csf_mapping", "does_not_exist.json"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Input file not found: does_not_exist.json" in captured.out


def test_csf_mapping_main_writes_expected_file(monkeypatch, capsys, tmp_path):
    data = make_input_assessment()
    input_file = tmp_path / "assessment.json"
    input_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["csf_mapping", str(input_file)])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 0
    assert "assessment_result_mapped.json" in captured.out
    assert (tmp_path / "data" / "output" / "assessment_result_mapped.json").exists()
