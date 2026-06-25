param(
    [string]$PythonScript = ".\scripts\generate-metrics.py",
    [string]$AssessmentInputFile = ".\assets\data\assessment-input.json",
    [string]$OutputFile = ".\outputs\metrics-output.json",
    [string]$CurrentFile = ".\assets\data\current-metrics.json",
    [string]$HistoryFile = ".\assets\data\validation-history.json",
    [string]$ChangeFile = ".\assets\data\formula-changelog.json",
    [switch]$AddFormulaChange,
    [string]$MetricName = "",
    [string]$ChangeSummary = "",
    [string]$Reason = "",
    [string]$Impact = "",
    [switch]$Commit,
    [switch]$Push,
    [string]$CommitMessage = "Run IACK pipeline update"
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $true
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-FileExists {
    param([string]$Path, [string]$Label)
    if (-not (Test-Path $Path)) {
        throw "$Label not found: $Path"
    }
}

function Ensure-ParentDirectory {
    param([string]$Path)
    $parent = Split-Path $Path -Parent
    if (-not [string]::IsNullOrWhiteSpace($parent) -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
}

function Load-JsonArray {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return @()
    }

    $raw = Get-Content $Path -Raw
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return @()
    }

    $parsed = $raw | ConvertFrom-Json
    if ($parsed -is [System.Collections.IEnumerable] -and $parsed -isnot [string]) {
        return @($parsed)
    }

    return @($parsed)
}

function Save-Json {
    param(
        [Parameter(Mandatory = $true)]$Data,
        [Parameter(Mandatory = $true)][string]$Path
    )

    Ensure-ParentDirectory -Path $Path

    if ($Data -is [System.Collections.IEnumerable] -and $Data -isnot [string]) {
        Set-Content -Path $Path -Encoding utf8 -Value (ConvertTo-Json -InputObject @($Data) -Depth 20)
    }
    else {
        Set-Content -Path $Path -Encoding utf8 -Value (ConvertTo-Json -InputObject $Data -Depth 20)
    }
}

Write-Step "Running Python metrics export"
Assert-FileExists -Path $PythonScript -Label "Python script"
Assert-FileExists -Path $AssessmentInputFile -Label "Assessment input file"

& python $PythonScript $AssessmentInputFile
if ($LASTEXITCODE -ne 0) {
    throw "Python script failed with exit code $LASTEXITCODE"
}

Write-Step "Verifying metrics output"
Assert-FileExists -Path $OutputFile -Label "Metrics output file"

Write-Step "Syncing current metrics"
$current = Get-Content $OutputFile -Raw | ConvertFrom-Json

if ($null -eq $current -or $null -eq $current.runId) {
    throw "Metrics output is invalid or missing runId."
}

Save-Json -Data $current -Path $CurrentFile

Write-Step "Appending validation history"
$historyEntry = [PSCustomObject]@{
    timestamp        = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    runId            = $current.runId
    score            = $current.overview.iackScore
    validationStatus = $current.overview.validationStatus
    confidence       = $current.overview.confidence
    testsPassed      = $current.validationLab.testsPassed
    testsFailed      = $current.validationLab.testsFailed
    duration         = $current.validationLab.duration
    source           = (Split-Path $OutputFile -Leaf)
}

$history = [System.Collections.ArrayList]@(Load-JsonArray -Path $HistoryFile)
[void]$history.Add($historyEntry)
Save-Json -Data @($history) -Path $HistoryFile

if ($AddFormulaChange) {
    Write-Step "Appending formula changelog entry"

    if ([string]::IsNullOrWhiteSpace($MetricName) -or
        [string]::IsNullOrWhiteSpace($ChangeSummary) -or
        [string]::IsNullOrWhiteSpace($Reason)) {
        throw "When -AddFormulaChange is used, -MetricName, -ChangeSummary, and -Reason are required."
    }

    $changeEntry = [PSCustomObject]@{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        metric    = $MetricName
        change    = $ChangeSummary
        reason    = $Reason
        impact    = $Impact
    }

    $changes = [System.Collections.ArrayList]@(Load-JsonArray -Path $ChangeFile)
    [void]$changes.Add($changeEntry)
    Save-Json -Data @($changes) -Path $ChangeFile
}

if ($Commit) {
    Write-Step "Committing changes to git"
    & git add .
    if ($LASTEXITCODE -ne 0) {
        throw "git add failed"
    }

    & git commit -m $CommitMessage
    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed"
    }
}

if ($Push) {
    Write-Step "Pushing changes to remote"
    & git push
    if ($LASTEXITCODE -ne 0) {
        throw "git push failed"
    }
}

Write-Step "Pipeline completed successfully"

Write-Step "Generating MITRE ATT&CK mapping"
$mitreScript = Join-Path $PSScriptRoot "generate-mitre-mapping.py"
if (-not (Test-Path $mitreScript)) {
    throw "Missing MITRE mapping generator: $mitreScript"
}

& python $mitreScript
if ($LASTEXITCODE -ne 0) {
    throw "MITRE mapping generation failed"
}

# IACK_ARTIFACT_INTEGRITY_GATE
Write-Host ""
Write-Host "==> Validating artifact integrity"
$manifestPath = Join-Path $PSScriptRoot "..\assets\data\iack-artifact-hashes.txt"
$artifactFiles = @(
    (Join-Path $PSScriptRoot "..\outputs\metrics-output.json"),
    (Join-Path $PSScriptRoot "..\assets\data\current-metrics.json"),
    (Join-Path $PSScriptRoot "..\assets\data\validation-history.json"),
    (Join-Path $PSScriptRoot "..\assets\data\iack-mitre-mapping.json")
)
foreach ($f in $artifactFiles) {
    if (-not (Test-Path $f)) { throw "Artifact integrity gate failed: missing file $f" }
}
$hashLines = foreach ($f in $artifactFiles) {
    $h = Get-FileHash $f -Algorithm SHA256
    "{0}  {1}" -f $h.Hash, $f
}
$hashLines | Set-Content $manifestPath -Encoding UTF8
foreach ($line in Get-Content $manifestPath) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split '\s{2,}', 2
    if ($parts.Count -ne 2) { throw "Artifact integrity gate failed: malformed manifest line '$line'" }
    $expected = $parts[0].Trim()
    $file = $parts[1].Trim()
    if (-not (Test-Path $file)) { throw "Artifact integrity gate failed: missing manifest file $file" }
    $actual = (Get-FileHash $file -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Artifact integrity gate failed: hash mismatch for $file" }
}
Write-Host "Artifact integrity validation passed."
