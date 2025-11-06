<#
Demo Capture — Green Jobs Brasil (Windows PowerShell)

Captura screenshots das páginas-chave e exporta o Playbook Visual em PDF
usando um navegador Chromium (Chrome ou Edge) em modo headless.

Uso:
  powershell -ExecutionPolicy Bypass -File .\scripts\demo_capture.ps1
  # opções
  powershell -ExecutionPolicy Bypass -File .\scripts\demo_capture.ps1 -Port 8002 -OutDir "docs\\demo-kit\\outputs"
#>

param(
  [int]$Port = 8002,
  [string]$OutDir = "docs\\demo-kit\\outputs"
)

$ErrorActionPreference = 'Stop'

function Write-Section($t){
  Write-Host "`n==========================" -ForegroundColor Cyan
  Write-Host " $t" -ForegroundColor White
  Write-Host "==========================`n" -ForegroundColor Cyan
}

function Get-ChromiumPath {
  $candidates = @(
    "$env:ProgramFiles\\Google\\Chrome\\Application\\chrome.exe",
    "$env:ProgramFiles(x86)\\Google\\Chrome\\Application\\chrome.exe",
    "$env:LocalAppData\\Google\\Chrome\\Application\\chrome.exe",
    "$env:ProgramFiles\\Microsoft\\Edge\\Application\\msedge.exe",
    "$env:ProgramFiles(x86)\\Microsoft\\Edge\\Application\\msedge.exe"
  ) | Where-Object { $_ -and (Test-Path $_) }

  if ($candidates.Count -gt 0) { return $candidates[0] }
  return $null
}

# 0) Preparação
Write-Section "Demo Capture"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# 1) Verificar API online
try {
  $status = Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri "http://127.0.0.1:$Port/api/status"
  if ($status.StatusCode -ne 200) { throw "API não respondeu com 200" }
  Write-Host "✅ API online: http://127.0.0.1:$Port" -ForegroundColor Green
} catch {
  Write-Host "❌ API offline. Inicie com: python start_api.py" -ForegroundColor Red
  exit 1
}

# 2) Localizar navegador Chromium
$browser = Get-ChromiumPath
if (-not $browser) {
  Write-Host "❌ Chrome/Edge não encontrado. Instale um navegador Chromium para captura headless." -ForegroundColor Red
  exit 1
}
Write-Host "Usando navegador: $browser" -ForegroundColor Green

# 3) Alvos de captura
$targets = @(
  @{ name = 'docs'; url = "http://127.0.0.1:$Port/docs" },
  @{ name = 'test-api'; url = "http://127.0.0.1:$Port/test-api" },
  @{ name = 'dashboard-empresa'; url = "http://127.0.0.1:$Port/empresas/dashboard" },
  @{ name = 'kpis'; url = "http://127.0.0.1:$Port/kpis" }
)

# 4) Capturar screenshots
Write-Section "Capturando screenshots"
foreach ($t in $targets) {
  $png = Join-Path $OutDir ("{0}.png" -f $t.name)
  Write-Host ("- " + $t.url) -ForegroundColor Yellow
  $args = @("--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1366,900", "--screenshot=$png", $t.url)
  try {
    Start-Process -FilePath $browser -ArgumentList $args -Wait -NoNewWindow
  } catch {
    # Fallback para --headless (legacy)
    $args = @("--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1366,900", "--screenshot=$png", $t.url)
    Start-Process -FilePath $browser -ArgumentList $args -Wait -NoNewWindow
  }
}

# 5) Exportar Playbook em PDF
Write-Section "Exportando Playbook (PDF)"
$pdf = Join-Path $OutDir "playbook.pdf"
$pdfUrl = "http://127.0.0.1:$Port/demo-playbook"
try {
  $argsPdf = @("--headless=new", "--disable-gpu", "--print-to-pdf=$pdf", $pdfUrl)
  Start-Process -FilePath $browser -ArgumentList $argsPdf -Wait -NoNewWindow
} catch {
  $argsPdf = @("--headless", "--disable-gpu", "--print-to-pdf=$pdf", $pdfUrl)
  Start-Process -FilePath $browser -ArgumentList $argsPdf -Wait -NoNewWindow
}

Write-Section "Concluído"
Write-Host "Arquivos gerados em: $OutDir" -ForegroundColor Green
Get-ChildItem -Path $OutDir | ForEach-Object { Write-Host (" - " + $_.Name) }
