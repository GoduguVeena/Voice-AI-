$ErrorActionPreference = "Stop"

$python = "C:\Users\G Veena\AppData\Local\Programs\Python\Python313\python.exe"
$upstream = Join-Path $PWD "external\FastSpeech2"

if (-not (Test-Path $upstream)) {
    New-Item -ItemType Directory -Force external | Out-Null
    git clone --depth 1 https://github.com/ming024/FastSpeech2.git $upstream
}

& $python -m pip install -r requirements.txt
& $python -m pip install -r (Join-Path $upstream "requirements.txt")
$env:FASTSPEECH2_ROOT = (Resolve-Path $upstream).Path

Write-Host "FASTSPEECH2_ROOT=$env:FASTSPEECH2_ROOT"
Write-Host "Environment ready for the English and Telugu wrapper scripts."