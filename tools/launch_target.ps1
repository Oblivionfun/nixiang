param(
  [Parameter(Mandatory=$true)][string]$SimulatorRoot,
  [Parameter(Mandatory=$true)][ValidatePattern('^[A-Za-z0-9._-]+$')][string]$SessionLabel
)

$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($SimulatorRoot)
$exe = Join-Path $root 'Jammers-simulator-full\jammers-simulator-full.exe'
if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
  throw "Simulator executable not found: $exe"
}

$out = Join-Path $PSScriptRoot "..\.local\launch\$SessionLabel"
New-Item -ItemType Directory -Force -Path $out | Out-Null
"label=$SessionLabel" | Set-Content -Encoding UTF8 (Join-Path $out 'launch.txt')
"executable_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $exe).Hash)" | Add-Content -Encoding UTF8 (Join-Path $out 'launch.txt')
"started_local=$([DateTime]::UtcNow.ToString('o'))" | Add-Content -Encoding UTF8 (Join-Path $out 'launch.txt')

# This starts only the locally installed program. It does not select a test mode,
# send API requests, inject code, or modify the simulator installation.
Start-Process -FilePath $exe -WorkingDirectory (Split-Path $exe)
Write-Host "Started local simulator for label $SessionLabel. Confirm the UI is PRACTICE before any test action."
