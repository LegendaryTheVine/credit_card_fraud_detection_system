$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$student = Join-Path $root 'student'
$bad = @()
# Solutions or instructor material must not appear in student/
$bad += Get-ChildItem $student -Recurse -Force |
    Where-Object { $_.FullName -match '(\\solutions\\|\\instructor\\|\\rubrics\\)' }
# Data and model binaries must not be committed
# (the local dataset in student\data\ is allowed: it is gitignored and publish skips it)
$bad += Get-ChildItem $student -Recurse -File -Force |
    Where-Object { $_.Extension -in '.csv','.pkl','.joblib' } |
    Where-Object { -not ($_.Extension -eq '.csv' -and $_.DirectoryName -eq (Join-Path $student 'data')) }
if ($bad.Count -gt 0) {
    $bad | ForEach-Object { Write-Host "Leak: $($_.FullName)" }
    exit 1
}
Write-Host "No leaks found in student/."
