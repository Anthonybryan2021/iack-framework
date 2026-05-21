import csv
import json

from iack.outputs.report_writer import write_csv, write_json, write_markdown


def make_result():
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
                "evidence_count": 3,
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
                "evidence_count": 2,
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
                "evidence_count": 1,
            },
        ],
    }


def test_write_json_creates_expected_file(tmp_path):
    output_path = tmp_path / "assessment_result.json"
    result = make_result()

    write_json(output_path, result)

    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["assessment_id"] == "IACK-TEST-0001"
    assert loaded["overall_weighted_score"] == 0.754
    assert len(loaded["metric_results"]) == 3


def test_write_csv_creates_expected_rows(tmp_path):
    output_path = tmp_path / "assessment_result.csv"
    result = make_result()

    write_csv(output_path, result["metric_results"])

    with output_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 3
    assert rows[0]["metric_id"] == "CONF-001"
    assert rows[1]["domain"] == "authenticity"
    assert rows[2]["passed"] == "False"


def test_write_markdown_creates_expected_sections(tmp_path):
    output_path = tmp_path / "assessment_result.md"
    result = make_result()

    write_markdown(output_path, result)

    content = output_path.read_text(encoding="utf-8")
    assert "# IACK Assessment Report: IACK-TEST-0001" in content
    assert "## Metric results" in content
    assert "| Metric ID | Metric Name | Domain | Score | Threshold | Passed | Confidence | Evidence Count |" in content
    assert "| CONF-001 | Confidentiality Control Strength | confidentiality | 0.82 | 0.7 | True | high | 3 |" in content

from iack.outputs.report_writer import main


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


def test_report_writer_main_returns_1_when_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["report_writer"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Usage: python -m iack.outputs.report_writer <input_json>" in captured.out


def test_report_writer_main_returns_1_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["report_writer", "does_not_exist.json"])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 1
    assert "Input file not found: does_not_exist.json" in captured.out


def test_report_writer_main_writes_expected_files(monkeypatch, capsys, tmp_path):
    data = make_input_assessment()
    input_file = tmp_path / "assessment.json"
    input_file.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["report_writer", str(input_file)])
    rc = main()
    captured = capsys.readouterr()

    assert rc == 0
    assert "Wrote:" in captured.out
    assert (tmp_path / "data" / "output" / "assessment_result.json").exists()
    assert (tmp_path / "data" / "output" / "assessment_result.csv").exists()
    assert (tmp_path / "data" / "output" / "assessment_result.md").exists()
