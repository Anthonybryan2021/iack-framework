import json
import sys
from pathlib import Path

from iack.metrics.model import score_assessment


DOMAIN_TO_CSF = {
    "confidentiality": {
        "csf_function": "Protect",
        "csf_code": "PR",
        "rationale": "Confidentiality safeguards align to data protection and access control outcomes."
    },
    "authenticity": {
        "csf_function": "Protect",
        "csf_code": "PR",
        "rationale": "Authenticity supports trusted identities, credentials, and protective safeguards."
    },
    "integrity": {
        "csf_function": "Detect",
        "csf_code": "DE",
        "rationale": "Integrity issues often require monitoring, verification, and detection of unauthorized changes."
    },
    "governance": {
        "csf_function": "Govern",
        "csf_code": "GV",
        "rationale": "Governance metrics align to risk strategy, policy, and oversight."
    },
    "asset_management": {
        "csf_function": "Identify",
        "csf_code": "ID",
        "rationale": "Asset understanding and risk context align to identification outcomes."
    },
}


def apply_csf_mapping(result: dict) -> dict:
    mapped_results = []

    for metric in result["metric_results"]:
        domain = metric["domain"]
        mapping = DOMAIN_TO_CSF.get(
            domain,
            {
                "csf_function": "Identify",
                "csf_code": "ID",
                "rationale": "Default mapping used until a domain-specific mapping is defined."
            },
        )

        enriched_metric = dict(metric)
        enriched_metric.update(mapping)
        mapped_results.append(enriched_metric)

    result_with_mapping = dict(result)
    result_with_mapping["metric_results"] = mapped_results
    return result_with_mapping


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m iack.mappings.csf_mapping <input_json>")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    with input_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    scored_result = score_assessment(data)
    mapped_result = apply_csf_mapping(scored_result)

    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "assessment_result_mapped.json"
    output_path.write_text(json.dumps(mapped_result, indent=2), encoding="utf-8-sig")

    print(f"Wrote: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
