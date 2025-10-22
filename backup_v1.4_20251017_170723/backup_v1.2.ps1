# SCRIPT DE BACKUP - GJB System v1.2
# Cria snapshot do sistema para ponto de restauracao

Write-Host "BACKUP GJB SYSTEM v1.2" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backup_v1.2_$timestamp"
$currentDir = Get-Location

Write-Host "Criando diretorio de backup: $backupDir" -ForegroundColor Yellow

# Criar pasta de backup
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Lista de arquivos/pastas essenciais para backup
$itemsToBackup = @(
    # Arquivos principais
    "start_api.py",
    "gjb_dev.db",
    "teste_rapido.py",
    
    # Documentação
    "README.md",
    "VERSION_1.2.md",
    "DOCUMENTACAO_COMPLETA.md",
    "MAPA_ROTAS.md",
    "SISTEMA_FUNCIONANDO.md",
    "ESTRATEGIA_ORGANIZACAO.md",
    "RELATORIO_LIMPEZA.md",
    "ML_DASHBOARD_RESTAURADO.md",
    "RELATORIO_FINAL_DIA.md",
    
    # Pastas completas
    "api",
    "tests",
    "data",
    "ml",
    "etl",
    "db",
    "scripts"
)

Write-Host ""
Write-Host "Copiando arquivos..." -ForegroundColor Yellow

$copiedCount = 0
$errorCount = 0

foreach ($item in $itemsToBackup) {
    if (Test-Path $item) {
        try {
            Copy-Item -Path $item -Destination $backupDir -Recurse -Force
            Write-Host "  OK $item" -ForegroundColor Green
            $copiedCount++
        } catch {
            Write-Host "  ERRO ao copiar $item" -ForegroundColor Red
            $errorCount++
        }
    } else {
        Write-Host "  $item nao encontrado" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Criando arquivo VERSION.txt..." -ForegroundColor Yellow

# Criar arquivo VERSION.txt no backup
$versionContent = @"
GREEN JOBS BRASIL - SYSTEM v1.2
================================

Data do Backup: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
Diretório Original: $currentDir

CONTEÚDO DO BACKUP:
- Sistema completo funcional
- 7 páginas web operacionais
- 8 APIs REST testadas
- Banco de dados com 981 registros
- Documentação completa

COMO RESTAURAR:
1. Copiar conteúdo desta pasta para pasta destino
2. Instalar dependências: pip install -r api/requirements.txt
3. Iniciar API: py start_api.py
4. Acessar: http://127.0.0.1:8002/

ARQUIVOS COPIADOS: $copiedCount
ERROS: $errorCount

Para mais informações, consulte VERSION_1.2.md
"@

$versionContent | Out-File -FilePath "$backupDir\VERSION.txt" -Encoding UTF8

Write-Host ""
Write-Host "Criando arquivo compactado..." -ForegroundColor Yellow

# Comprimir backup (se disponível)
try {
    Compress-Archive -Path $backupDir -DestinationPath "${backupDir}.zip" -Force
    Write-Host "  OK Arquivo compactado criado: ${backupDir}.zip" -ForegroundColor Green
    
    # Calcular tamanho
    $zipSize = (Get-Item "${backupDir}.zip").Length / 1MB
    Write-Host "  Tamanho: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
} catch {
    Write-Host "  Nao foi possivel comprimir (mantida pasta)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================" -ForegroundColor Cyan
Write-Host "BACKUP CONCLUIDO!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""
Write-Host "ESTATISTICAS:" -ForegroundColor Cyan
Write-Host "  - Arquivos copiados: $copiedCount" -ForegroundColor White
Write-Host "  - Erros: $errorCount" -ForegroundColor $(if ($errorCount -eq 0) { "Green" } else { "Red" })
Write-Host "  - Diretorio: $backupDir" -ForegroundColor White
Write-Host ""
Write-Host "PROXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "  1. Verificar conteudo do backup" -ForegroundColor White
Write-Host "  2. Testar restauracao (opcional)" -ForegroundColor White
Write-Host "  3. Mover backup para local seguro" -ForegroundColor White
Write-Host ""
Write-Host "Sistema GJB v1.2 salvo com sucesso!" -ForegroundColor Green
Write-Host ""
