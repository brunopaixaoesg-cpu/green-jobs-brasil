<#
Demonstration Orchestrator — Green Jobs Brasil (Windows PowerShell)

What it does:
1) Checks Python and installs dependencies if needed
2) Ensures uploads folders exist
3) Frees port 8002 if occupied
4) Starts API (uvicorn api.main:app) on 127.0.0.1:8002
5) Waits until API is ready (/api/status)
6) Seeds demo data (endpoint /api/populate or fallback to scripts/popular_dados_demo.py)
7) Runs a short smoke test (scripts/full_smoke_test.py)
8) Opens key pages (docs, /test-api, dashboards)

Run:
  powershell -ExecutionPolicy Bypass -File .\scripts\demo_playbook.ps1
#>

param(
    [switch]$ReinstallDeps,
    [int]$Port = 8002
)

function Write-Section($title) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $title" -ForegroundColor White
    Write-Host "========================================`n" -ForegroundColor Cyan
}

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $root

Write-Section "Green Jobs Brasil — Demo Orchestrator"

# 1) Python check and deps
try {
    $pyVersion = & python --version 2>$null
    if (-not $pyVersion) { throw "Python não encontrado no PATH" }
    Write-Host "Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale Python 3.13+ e tente novamente." -ForegroundColor Red
    exit 1
}

if ($ReinstallDeps) {
    Write-Section "Instalando dependências"
    try {
        if (Test-Path "$root\requirements.txt") {
            Write-Host "Instalando requirements.txt (raiz)" -ForegroundColor Yellow
            python -m pip install -r "$root\requirements.txt"
        }
        if (Test-Path "$root\api\requirements.txt") {
            Write-Host "Instalando api/requirements.txt" -ForegroundColor Yellow
            python -m pip install -r "$root\api\requirements.txt"
        }
    } catch {
        Write-Host "⚠️  Falha parcial na instalação, seguindo adiante..." -ForegroundColor Yellow
    }
}

# 2) Upload folders
Write-Section "Garantindo pastas de upload"
$uploadDirs = @(
    "api\static\uploads\profissionais",
    "api\static\uploads\empresas"
)
foreach ($d in $uploadDirs) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
Write-Host "Pastas criadas/ok" -ForegroundColor Green

# 3) Free port if busy
Write-Section "Liberando porta $Port (se necessário)"
$net = netstat -ano | findstr :$Port | Select-String -NotMatch "LISTENING" -Quiet 2>$null
# Show listening entries and kill python if bound
$bindings = netstat -ano | findstr ":$Port" | Select-String "LISTENING" 2>$null
if ($bindings) {
    (netstat -ano | findstr ":$Port" | Select-String "LISTENING").ToString().Split() | ForEach-Object {
        if ($_ -match '^[0-9]+$') {
            try { taskkill /F /PID $_ | Out-Null } catch {}
        }
    }
    Start-Sleep -Seconds 1
    Write-Host "Porta liberada." -ForegroundColor Green
} else {
    Write-Host "Porta livre." -ForegroundColor Green
}

# 4) Start API
Write-Section "Iniciando API (uvicorn)"
$apiCmd = "-m uvicorn api.main:app --host 127.0.0.1 --port $Port --reload"
Start-Process -FilePath "python" -ArgumentList $apiCmd -WindowStyle Minimized
Start-Sleep -Seconds 1

# 5) Wait until API is ready
Write-Host "Aguardando API ficar online..." -ForegroundColor Yellow
$ready = $false
for ($i=0; $i -lt 30; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/status" -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 1
}
if (-not $ready) {
    Write-Host "❌ API não respondeu a tempo." -ForegroundColor Red
    exit 1
}
Write-Host "✅ API online em http://127.0.0.1:$Port" -ForegroundColor Green

# 6) Seed demo data
Write-Section "Populando dados demo"
$seedOk = $false
try {
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/populate" -UseBasicParsing -TimeoutSec 10
    if ($resp.StatusCode -eq 200) { $seedOk = $true }
} catch {}
if (-not $seedOk) {
    try {
        Write-Host "Endpoint indisponível, executando scripts/popular_dados_demo.py" -ForegroundColor Yellow
        python "scripts/popular_dados_demo.py"
        $seedOk = $true
    } catch {
        Write-Host "⚠️  Não foi possível popular automaticamente." -ForegroundColor Yellow
    }
}
if ($seedOk) { Write-Host "✅ Base populada" -ForegroundColor Green }

# 7) Short smoke test (não falha a pipeline)
Write-Section "Smoke test rápido"
try {
    python "scripts/full_smoke_test.py"
} catch {
    Write-Host "⚠️  Smoke test com falhas (prosseguindo para demo)" -ForegroundColor Yellow
}

# 8) Open browser tabs
Write-Section "Abrindo páginas da demonstração"
$urls = @(
    "http://127.0.0.1:$Port/docs",
    "http://127.0.0.1:$Port/api/kpis/gerais",
    "http://127.0.0.1:$Port/test-api",
    "http://127.0.0.1:$Port/empresas/dashboard",
    "http://127.0.0.1:$Port/vagas",
    "http://127.0.0.1:$Port/kpis"
)
foreach ($u in $urls) { Start-Process $u }

Write-Host "`n✅ Pronto! Demonstração em execução." -ForegroundColor Green
Write-Host "➡️  Se precisar parar, feche a janela do Uvicorn ou encerre o processo Python." -ForegroundColor Gray
