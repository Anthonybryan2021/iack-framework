import json
import sys
from pathlib import Path


def confidence_from_evidence_count(evidence_count: int) -> str:
    if evidence_count >= 3:
        return "high"
    if evidence_count == 2:
        return "medium"
    return "low"


def score_assessment(data: dict) -> dict:
    metrics = data["metrics"]
    weighted_score = 0.0
    scored_metrics = []

    passed_metrics = 0
    failed_metrics = 0

    for metric in metrics:
        score = float(metric["score"])
        weight = float(metric["weight"])
        threshold = float(metric["threshold"])
        evidence = metric.get("evidence", [])

        weighted_score += score * weight
        passed = score >= threshold
        confidence = confidence_from_evidence_count(len(evidence))

        if passed:
            passed_metrics += 1
        else:
            failed_metrics += 1

        scored_metrics.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "domain": metric["domain"],
                "score": round(score, 4),
                "weight": round(weight, 4),
                "threshold": round(threshold, 4),
                "passed": passed,
                "confidence": confidence,
                "evidence_count": len(evidence),
            }
        )

    return {
        "assessment_id": data["assessment_id"],
        "system_name": data["system_name"],
        "assessment_date": data["assessment_date"],
        "overall_weighted_score": round(weighted_score, 4),
        "metrics_passed": passed_metrics,
        "metrics_failed": failed_metrics,
        "metric_results": scored_metrics,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m iack.metrics.model <input_json>")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result = score_assessment(data)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
