import csv
import json
import sys
from pathlib import Path

from iack.metrics.model import score_assessment


def write_json(output_path: Path, data: dict) -> None:
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_csv(output_path: Path, metric_results: list[dict]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "metric_id",
                "metric_name",
                "domain",
                "score",
                "weight",
                "threshold",
                "passed",
                "confidence",
                "evidence_count",
            ],
        )
        writer.writeheader()
        writer.writerows(metric_results)


def write_markdown(output_path: Path, result: dict) -> None:
    lines = [
        f"# IACK Assessment Report: {result['assessment_id']}",
        "",
        f"- System: {result['system_name']}",
        f"- Assessment date: {result['assessment_date']}",
        f"- Overall weighted score: {result['overall_weighted_score']}",
        f"- Metrics passed: {result['metrics_passed']}",
        f"- Metrics failed: {result['metrics_failed']}",
        "",
        "## Metric results",
        "",
        "| Metric ID | Metric Name | Domain | Score | Threshold | Passed | Confidence | Evidence Count |",
        "|---|---|---|---:|---:|---|---|---:|",
    ]

    for metric in result["metric_results"]:
        lines.append(
            f"| {metric['metric_id']} | {metric['metric_name']} | {metric['domain']} | "
            f"{metric['score']} | {metric['threshold']} | {metric['passed']} | "
            f"{metric['confidence']} | {metric['evidence_count']} |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m iack.outputs.report_writer <input_json>")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    result = score_assessment(data)

    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    write_json(output_dir / "assessment_result.json", result)
    write_csv(output_dir / "assessment_result.csv", result["metric_results"])
    write_markdown(output_dir / "assessment_result.md", result)

    print("Wrote:")
    print("- data/output/assessment_result.json")
    print("- data/output/assessment_result.csv")
    print("- data/output/assessment_result.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

