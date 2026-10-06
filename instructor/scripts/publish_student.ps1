param(
    [Parameter(Mandatory=$true)][string]$Target
)
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
& (Join-Path $PSScriptRoot 'check_no_leaks.ps1')
if ($LASTEXITCODE -ne 0) { throw 'Leak check failed; aborting.' }
if (-not (Test-Path $Target)) { New-Item -ItemType Directory -Path $Target | Out-Null }
# Mirror student/ into the target, keeping the target's .git folder and skipping local data/model files
robocopy (Join-Path $root 'student') $Target /MIR /XD .git __pycache__ .ipynb_checkpoints /XF *.csv *.pkl *.joblib | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }
Write-Host "Published student/ to $Target. Review, commit and push from there."
