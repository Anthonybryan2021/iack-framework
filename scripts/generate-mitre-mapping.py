#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
CURRENT_METRICS = ROOT / "assets" / "data" / "current-metrics.json"
RULES_FILE = ROOT / "assets" / "data" / "iack-attack-rules.json"
OUTPUT_FILE = ROOT / "assets" / "data" / "iack-mitre-mapping.json"

NAME_TO_METRIC_ID = {
    "Integrity": "I1",
    "Authenticity": "A1",
    "Confidentiality": "C1",
    "Key Management": "K1"
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def normalize_status(value):
    if value is None:
        return "Unknown"
    text = str(value).strip()
    return text if text else "Unknown"

def normalize_rating(score):
    try:
        s = float(score)
    except Exception:
        return "unknown"
    if s >= 85:
        return "good"
    if s >= 70:
        return "moderate"
    return "needs-improvement"

def get_top_level(data, *keys, default=None):
    for key in keys:
        if key in data:
            return data[key]
    return default

def pillar_lookup(current):
    pillars = {}

    overview = current.get("overview", {})
    raw_pillars = overview.get("pillars", []) if isinstance(overview, dict) else []

    if isinstance(raw_pillars, list):
        for item in raw_pillars:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            metric_id = NAME_TO_METRIC_ID.get(name)
            if metric_id:
                pillars[metric_id] = {
                    "metric_id": metric_id,
                    "name": name,
                    "score": item.get("score"),
                    "status": item.get("status")
                }

    raw_assessment = current.get("rawAssessment", {})
    metric_results = raw_assessment.get("metric_results", []) if isinstance(raw_assessment, dict) else []

    if isinstance(metric_results, list):
        for item in metric_results:
            if not isinstance(item, dict):
                continue
            metric_id = item.get("metric_id")
            if not metric_id:
                continue

            existing = pillars.get(metric_id, {})
            merged = dict(existing)
            merged.update({
                "metric_id": metric_id,
                "metric_name": item.get("metric_name"),
                "domain": item.get("domain"),
                "score": item.get("score", existing.get("score")),
                "confidence": item.get("confidence", existing.get("confidence")),
                "passed": item.get("passed")
            })
            pillars[metric_id] = merged

    return pillars

def build():
    current = load_json(CURRENT_METRICS)
    rules = load_json(RULES_FILE)

    pillars = pillar_lookup(current)
    items = []

    overview = current.get("overview", {}) if isinstance(current.get("overview", {}), dict) else {}

    overall_score = overview.get(
        "iackScore",
        get_top_level(current, "overall_score", "overallScore", default=0)
    )
    validation = overview.get(
        "validationStatus",
        get_top_level(current, "validation", "validationStatus", default="Unknown")
    )
    open_findings = overview.get(
        "openFindings",
        get_top_level(current, "open_findings", "openFindings", default=0)
    )
    next_action = overview.get(
        "nextAction",
        get_top_level(
            current,
            "next_action",
            "nextAction",
            default="Review ATT&CK alignment and defensive action coverage."
        )
    )

    for rule in rules.get("rules", []):
        metric_id = rule["metric_id"]
        metric_name = rule["metric_name"]
        pillar = pillars.get(metric_id, {})

        pillar_score = pillar.get("pillar_score", pillar.get("score", overall_score))
        if isinstance(pillar_score, float) and pillar_score <= 1:
            pillar_score = round(pillar_score * 100)

        raw_status = pillar.get("status")
        if raw_status in ("good", "moderate", "needs-improvement"):
            status = "Validated" if raw_status == "good" else "Review"
        else:
            status = normalize_status(
                raw_status if raw_status is not None else (
                    "Validated" if pillar.get("passed") is True
                    else "Review" if pillar.get("passed") is False
                    else "Validated" if str(validation).lower() == "passed"
                    else "Review"
                )
            )

        confidence = pillar.get(
            "confidence",
            "High" if str(validation).lower() == "passed" else "Medium"
        )
        if isinstance(confidence, str):
            confidence = confidence.capitalize()

        pillar_rating = pillar.get("pillar_rating", normalize_rating(pillar_score))

        items.append({
            "metric_id": metric_id,
            "metric_name": metric_name,
            "attack_tactic": rule["attack_tactic"],
            "attack_technique_id": rule["attack_technique_id"],
            "attack_technique_name": rule["attack_technique_name"],
            "confidence": confidence,
            "recommendation": rule["default_recommendation"],
            "owner": rule.get("owner", "Unassigned"),
            "status": status,
            "pillar_score": pillar_score,
            "pillar_rating": pillar_rating
        })

    output = {
        "framework": "IACK",
        "mapping_version": rules.get("rules_version", "v0.1"),
        "generated_at": utc_now(),
        "source_metrics": "./assets/data/current-metrics.json",
        "source_rules": "./assets/data/iack-attack-rules.json",
        "overall_score": overall_score,
        "validation": validation,
        "open_findings": open_findings,
        "next_action": next_action,
        "items": items
    }

    OUTPUT_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    build()
