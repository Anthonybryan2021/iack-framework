[CmdletBinding()]
param(
    [string]$InputPath = ".\data\input\sample_assessment.json"
)

python -m iack.validators.assessment_validator $InputPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m iack.metrics.model $InputPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m iack.outputs.report_writer $InputPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m iack.mappings.csf_mapping $InputPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "IACK assessment workflow completed successfully."
