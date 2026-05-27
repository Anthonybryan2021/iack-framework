param(
    [string]$OutputFile = ".\assets\data\assessment-input.json",
    [string]$PipelineScript = ".\scripts\run-iack-pipeline.ps1",
    [string]$PythonScript = ".\scripts\generate-metrics.py",
    [switch]$RunPipeline,
    [switch]$Commit,
    [switch]$Push,
    [string]$CommitMessage = ""
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Ensure-ParentDirectory {
    param([string]$Path)
    $parent = Split-Path $Path -Parent
    if (-not [string]::IsNullOrWhiteSpace($parent) -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
}

function Read-NonEmptyOrDefault {
    param(
        [string]$Prompt,
        [string]$DefaultValue
    )

    $value = Read-Host $Prompt
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $DefaultValue
    }

    return $value
}

function Read-Score {
    param([string]$Prompt)

    while ($true) {
        $value = Read-Host $Prompt
        $parsed = 0.0

        if ([double]::TryParse($value, [ref]$parsed)) {
            if ($parsed -ge 0 -and $parsed -le 1) {
                return $parsed
            }
        }

        Write-Host "Enter a decimal score between 0 and 1, for example 0.82" -ForegroundColor Yellow
    }
}

Write-Step "Build assessment input"

$defaultAssessmentId = "assess-$(Get-Date -Format 'yyyyMMddHHmmss')"
$assessmentId = Read-NonEmptyOrDefault -Prompt "Assessment ID" -DefaultValue $defaultAssessmentId
$systemName = Read-NonEmptyOrDefault -Prompt "System name" -DefaultValue "IACK Framework"

$integrityScore = Read-Score -Prompt "Integrity score (0-1)"
$authenticityScore = Read-Score -Prompt "Authenticity score (0-1)"
$confidentialityScore = Read-Score -Prompt "Confidentiality score (0-1)"
$keyManagementScore = Read-Score -Prompt "Key Management score (0-1)"

$assessment = [PSCustomObject]@{
    assessment_id   = $assessmentId
    system_name     = $systemName
    assessment_date = (Get-Date).ToString("yyyy-MM-dd")
    metrics         = @(
        [PSCustomObject]@{
            metric_id   = "I1"
            metric_name = "Integrity Controls"
            domain      = "Integrity"
            score       = $integrityScore
            weight      = 0.25
            threshold   = 0.70
            evidence    = @("hash validation", "config review", "audit log")
        },
        [PSCustomObject]@{
            metric_id   = "A1"
            metric_name = "Authenticity Validation"
            domain      = "Authenticity"
            score       = $authenticityScore
            weight      = 0.25
            threshold   = 0.70
            evidence    = @("certificate check", "identity proof")
        },
        [PSCustomObject]@{
            metric_id   = "C1"
            metric_name = "Confidentiality Safeguards"
            domain      = "Confidentiality"
            score       = $confidentialityScore
            weight      = 0.25
            threshold   = 0.70
            evidence    = @("encryption review", "access control", "data handling")
        },
        [PSCustomObject]@{
            metric_id   = "K1"
            metric_name = "Key Management"
            domain      = "Key Management"
            score       = $keyManagementScore
            weight      = 0.25
            threshold   = 0.70
            evidence    = @("rotation policy", "vault config", "recovery test")
        }
    )
}

Ensure-ParentDirectory -Path $OutputFile
$assessment | ConvertTo-Json -Depth 10 | Set-Content -Path $OutputFile -Encoding utf8

Write-Host "Wrote $OutputFile" -ForegroundColor Green

if ($RunPipeline) {
    Write-Step "Run pipeline"

    if (-not (Test-Path $PipelineScript)) {
        throw "Pipeline script not found: $PipelineScript"
    }

    if (-not (Test-Path $PythonScript)) {
        throw "Python script not found: $PythonScript"
    }

    & $PipelineScript `
        -PythonScript $PythonScript `
        -AssessmentInputFile $OutputFile `
        -Commit:$Commit `
        -Push:$Push `
        -CommitMessage $CommitMessage
}
else {
    Write-Host "Pipeline not run. Use -RunPipeline to execute the workflow after generating input." -ForegroundColor Yellow
}