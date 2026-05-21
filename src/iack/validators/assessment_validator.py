import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = ["assessment_id", "system_name", "assessment_date", "metrics"]
REQUIRED_METRIC_FIELDS = [
    "metric_id",
    "metric_name",
    "domain",
    "weight",
    "threshold",
    "confidence_rule",
    "score",
    "evidence",
]


def validate_assessment(data: dict) -> list[str]:
    errors = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"Missing top-level field: {field}")

    metrics = data.get("metrics", [])
    if not isinstance(metrics, list) or not metrics:
        errors.append("metrics must be a non-empty list")
        return errors

    total_weight = 0.0

    for index, metric in enumerate(metrics, start=1):
        for field in REQUIRED_METRIC_FIELDS:
            if field not in metric:
                errors.append(f"Metric #{index} missing field: {field}")

        metric_id = metric.get("metric_id", f"Metric #{index}")
        weight = metric.get("weight")
        threshold = metric.get("threshold")
        score = metric.get("score")
        evidence = metric.get("evidence", [])

        if isinstance(weight, (int, float)):
            total_weight += weight
            if not 0 <= weight <= 1:
                errors.append(f"{metric_id} weight must be between 0 and 1")
        else:
            errors.append(f"{metric_id} weight must be numeric")

        if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
            errors.append(f"{metric_id} threshold must be between 0 and 1")

        if not isinstance(score, (int, float)) or not 0 <= score <= 1:
            errors.append(f"{metric_id} score must be between 0 and 1")

        if not isinstance(evidence, list):
            errors.append(f"{metric_id} evidence must be a list")
        elif len(evidence) == 0:
            errors.append(f"{metric_id} must include at least one evidence item")

    if round(total_weight, 2) != 1.00:
        errors.append(f"Metric weights must sum to 1.00, got {total_weight:.2f}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m iack.validators.assessment_validator <input_json>")
        return 1

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    errors = validate_assessment(data)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
