$pythonPath = "C:\Users\ggwza\Anaconda3\python.exe"
$scriptPath = Join-Path $PSScriptRoot "run.py"

if (-not (Test-Path $pythonPath)) {
    Write-Host "[ERROR] Python not found: $pythonPath"
    Read-Host "Press Enter to exit"
    exit 1
}

& $pythonPath $scriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Program exited with code: $LASTEXITCODE"
    Read-Host "Press Enter to exit"
}
