# SCRIPT DE LIMPEZA - GREEN JOBS BRASIL
# Remove arquivos redundantes e organiza estrutura

Write-Host "LIMPEZA E ORGANIZACAO - GREEN JOBS BRASIL" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$removidos = 0
$erros = 0

# Funcao para remover arquivo com verificacao
function Remove-Safe {
    param($path)
    if (Test-Path $path) {
        try {
            Remove-Item $path -Force
            Write-Host "OK Removido: $path" -ForegroundColor Green
            $script:removidos++
        } catch {
            Write-Host "ERRO ao remover: $path" -ForegroundColor Red
            $script:erros++
        }
    } else {
        Write-Host "NAO existe: $path" -ForegroundColor Yellow
    }
}

Write-Host "FASE 1: Criar pasta tests/" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan

# Criar pasta tests se nao existir
if (-not (Test-Path "tests")) {
    New-Item -ItemType Directory -Path "tests" -Force | Out-Null
    Write-Host "OK Pasta tests/ criada" -ForegroundColor Green
} else {
    Write-Host "JA EXISTE Pasta tests/" -ForegroundColor Yellow
}

# Mover arquivos de teste
$testFiles = @(
    "auditoria_completa.py",
    "test_api_completo.py",
    "test_cnpj.py"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        try {
            Move-Item $file "tests/" -Force
            Write-Host "OK Movido: $file -> tests/" -ForegroundColor Green
        } catch {
            Write-Host "JA EXISTE em tests/: $file" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "FASE 2: Remover APIs duplicadas" -ForegroundColor Cyan
Write-Host "--------------------------------" -ForegroundColor Cyan

$apisRedundantes = @(
    "api_empresas.py",
    "api_simples.py",
    "api_teste.py",
    "api/sqlite_api.py"
)

foreach ($file in $apisRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 3: Remover scripts de teste duplicados" -ForegroundColor Cyan
Write-Host "--------------------------------------------" -ForegroundColor Cyan

$testesRedundantes = @(
    "test_api.py",
    "test_dashboard.py",
    "test_search.py",
    "test_sistema.py",
    "teste_sistema_completo.py",
    "test_ml_sistema.py"
)

foreach ($file in $testesRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 4: Remover scripts start redundantes" -ForegroundColor Cyan
Write-Host "------------------------------------------" -ForegroundColor Cyan

$startRedundantes = @(
    "start_api_ml.py",
    "start_ml_api.py",
    "start_debug.bat"
)

foreach ($file in $startRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 5: Remover scripts debug/demo" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Cyan

$debugFiles = @(
    "api_debug.py",
    "demo_sistema.py",
    "check_all_tables.py",
    "check_companies.py"
)

foreach ($file in $debugFiles) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 6: Remover documentação redundante" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$docsRedundantes = @(
    "STATUS_FINAL_PROJETO.md",
    "ESTRATEGIA_FOLLOWUP.md",
    "MATERIAL_APRESENTACAO.md",
    "MAPEAMENTO_CONTATOS.md",
    "relatorio_executivo.html"
)

foreach ($file in $docsRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 7: Remover templates duplicados" -ForegroundColor Cyan
Write-Host "-------------------------------------" -ForegroundColor Cyan

$templatesRedundantes = @(
    "api/templates/dashboard.html",
    "api/templates/dashboard_demo.html",
    "api/templates/dashboard_final.html",
    "api/templates/cnaes_modernos.html"
)

foreach ($file in $templatesRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 8: Remover scripts geradores redundantes" -ForegroundColor Cyan
Write-Host "----------------------------------------------" -ForegroundColor Cyan

$geradoresRedundantes = @(
    "scripts/gerar_profissionais_fake.py",
    "scripts/gerar_profissionais_simples.py",
    "scripts/gerar_vagas_esg.py",
    "scripts/gerar_candidaturas.py",
    "scripts/gerar_candidaturas_vagas_ambientais.py"
)

foreach ($file in $geradoresRedundantes) {
    Remove-Safe $file
}

Write-Host ""
Write-Host "FASE 9: Limpar __pycache__" -ForegroundColor Cyan
Write-Host "--------------------------" -ForegroundColor Cyan

$pycaches = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__"
$pycacheCount = 0

foreach ($pycache in $pycaches) {
    try {
        Remove-Item $pycache.FullName -Recurse -Force
        Write-Host "OK Removido: $($pycache.FullName)" -ForegroundColor Green
        $pycacheCount++
    } catch {
        Write-Host "ERRO: $($pycache.FullName)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "LIMPEZA CONCLUIDA!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "ESTATISTICAS:" -ForegroundColor Cyan
Write-Host "  Arquivos removidos: $removidos" -ForegroundColor White
Write-Host "  __pycache__ removidos: $pycacheCount" -ForegroundColor White
Write-Host "  Erros: $erros" -ForegroundColor $(if ($erros -eq 0) { "Green" } else { "Red" })
Write-Host ""
Write-Host "PROXIMO PASSO:" -ForegroundColor Cyan
Write-Host "  cd tests" -ForegroundColor Yellow
Write-Host "  py auditoria_completa.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para iniciar API:" -ForegroundColor Cyan
Write-Host "  Start-Process powershell -ArgumentList `"-NoExit`", `"-Command`", `"cd 'C:\Users\Bruno\Empresas Verdes'; py -m uvicorn api.sqlite_api_clean:app --host 127.0.0.1 --port 8002`"" -ForegroundColor Yellow
Write-Host ""
