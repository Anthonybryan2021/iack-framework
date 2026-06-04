# IACK Framework

IACK is an Integrity-Authenticity-Confidentiality-Key management framework for cybersecurity assessment and validation.

## Install

```powershell
python -m pip install -e .
```

## Import

```python
from iack.metrics import model
from iack.validators import assessment_validator
from iack.mappings import csf_mapping
from iack.outputs import report_writer
```

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
