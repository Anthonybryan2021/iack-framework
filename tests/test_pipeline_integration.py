import csv
import json

from iack.mappings.csf_mapping import apply_csf_mapping
from iack.metrics.model import score_assessment
from iack.outputs.report_writer import write_csv, write_json, write_markdown
from iack.validators.assessment_validator import validate_assessment


def make_valid_assessment():
    return {
        "assessment_id": "IACK-INTEG-0001",
        "system_name": "Integration Test System",
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


def test_full_pipeline_integration(tmp_path):
    data = make_valid_assessment()

    errors = validate_assessment(data)
    assert errors == []

    scored = score_assessment(data)
    assert scored["assessment_id"] == "IACK-INTEG-0001"
    assert scored["metrics_passed"] == 2
    assert scored["metrics_failed"] == 1

    mapped = apply_csf_mapping(scored)
    assert len(mapped["metric_results"]) == 3
    assert any(metric["csf_code"] == "PR" for metric in mapped["metric_results"])
    assert any(metric["csf_code"] == "DE" for metric in mapped["metric_results"])

    json_path = tmp_path / "assessment_result.json"
    csv_path = tmp_path / "assessment_result.csv"
    md_path = tmp_path / "assessment_result.md"

    write_json(json_path, mapped)
    write_csv(csv_path, scored["metric_results"])
    write_markdown(md_path, mapped)

    assert json_path.exists()
    assert csv_path.exists()
    assert md_path.exists()

    loaded_json = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded_json["overall_weighted_score"] == 0.754
    assert loaded_json["metric_results"][0]["csf_code"] in {"PR", "DE", "GV", "ID"}

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert "csf_code" not in rows[0]

    markdown = md_path.read_text(encoding="utf-8")
    assert "# IACK Assessment Report: IACK-INTEG-0001" in markdown
    assert "## Metric results" in markdown
