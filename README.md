# IACK Framework

IACK is an Integrity-Authenticity-Confidentiality-Key management framework for cybersecurity assessment and validation.

## Install

```powershell
python -m pip install -e .
```

## Assessment flow

```python
from iack.validators.assessment_validator import validate_assessment
from iack.mappings.csf_mapping import map_to_csf
from iack.metrics.model import compute_iack_metrics
from iack.outputs.report_writer import write_report
```

1. Load an assessment input.
2. Validate the structure and values.
3. Map findings to a framework view.
4. Compute IACK metrics.
5. Write the report output.

## Example inputs

- `examples/assessment-input.json`
- `examples/expected-output.json`

## Run tests

```powershell
pytest
```

## Package layout

The package is distributed from `src/iack/` only. Legacy root-level modules are not part of the wheel.

## Notes

CLI entry points will be added later, after the assessment pipeline stabilizes.
