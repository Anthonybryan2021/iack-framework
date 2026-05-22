# IACK Framework

IACK is an Integrity-Authenticity-Confidentiality-Key management framework for cybersecurity assessment and validation.

## Install

```powershell
python -m pip install -e .
```

## CLI usage

The IACK package exposes four CLI commands for validation, scoring, CSF mapping, and report generation.

```powershell
python -m pip install -e .
iack-validate .\examples\assessment-input.json
iack-score .\examples\assessment-input.json
iack-map-csf .\examples\assessment-input.json
iack-report .\examples\assessment-input.json
```

### Output files

- `data/output/assessment_result.json`
- `data/output/assessment_result.csv`
- `data/output/assessment_result.md`
- `data/output/assessment_result_mapped.json`

## Assessment flow

```python
import json
from pathlib import Path

from iack.validators.assessment_validator import validate_assessment
from iack.metrics.model import score_assessment
from iack.mappings.csf_mapping import apply_csf_mapping
from iack.outputs.report_writer import write_json, write_csv, write_markdown

input_path = Path("examples/assessment-input.json")
data = json.loads(input_path.read_text(encoding="utf-8-sig"))

errors = validate_assessment(data)
if errors:
    raise ValueError(f"Assessment validation failed: {errors}")

result = score_assessment(data)
mapped_result = apply_csf_mapping(result)

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

write_json(output_dir / "assessment_result.json", mapped_result)
write_csv(output_dir / "assessment_result.csv", mapped_result["metric_results"])
write_markdown(output_dir / "assessment_result.md", mapped_result)
```

## Example inputs

- `examples/assessment-input.json`
- `examples/expected-output.json`

## Run tests

```powershell
pytest
```

## Package layout

The installable package lives under `src/iack/`. Root-level files such as `README.md`, `pyproject.toml`, `tests/`, and `examples/` support packaging, documentation, and validation.
