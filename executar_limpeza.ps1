# Script de limpeza completo - Green Jobs Brasil
# Data: 01/11/2025
# Objetivo: Organizar estrutura e remover duplicatas

Write-Host "🧹 Iniciando limpeza do projeto Green Jobs Brasil..." -ForegroundColor Green
Write-Host ""

# Confirmar antes de executar
$confirmacao = Read-Host "⚠️  Este script vai mover e remover arquivos. Deseja continuar? (s/n)"
if ($confirmacao -ne "s" -and $confirmacao -ne "S") {
    Write-Host "❌ Limpeza cancelada." -ForegroundColor Red
    exit
}

$erros = 0
$avisos = 0

# =========================================
# Fase 1: Criar estrutura de pastas
# =========================================
Write-Host "`n📁 Fase 1: Criando estrutura de pastas..." -ForegroundColor Cyan

$pastas = @(
    "scripts\analise",
    "scripts\debug",
    "scripts\demo",
    "scripts\migrations",
    "scripts\populacao",
    "tests\frontend",
    "docs\archived"
)

foreach ($pasta in $pastas) {
    try {
        New-Item -ItemType Directory -Path $pasta -Force | Out-Null
        Write-Host "  ✓ Criada: $pasta" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Erro ao criar $pasta : $_" -ForegroundColor Yellow
        $avisos++
    }
}

# =========================================
# Fase 2: Remover backups e duplicatas
# =========================================
Write-Host "`n🗑️  Fase 2: Removendo backups e arquivos duplicados..." -ForegroundColor Cyan

$arquivosRemover = @(
    "backup_v1.2_20251016_205417.zip",
    "backup_v1.3_auth_20251016_220802.zip",
    "backup_v1.4_20251017_170723.rar",
    "README_OLD.md",
    "DOCUMENTACAO_COMPLETA.md",
    "STATUS_FINAL_PROJETO.md",
    "SISTEMA_FUNCIONANDO.md",
    "SISTEMA_COMPLETO_FINAL.md"
)

foreach ($arquivo in $arquivosRemover) {
    if (Test-Path $arquivo) {
        try {
            Remove-Item $arquivo -Force
            Write-Host "  ✓ Removido: $arquivo" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao remover $arquivo : $_" -ForegroundColor Red
            $erros++
        }
    } else {
        Write-Host "  ⊘ Não encontrado: $arquivo" -ForegroundColor Gray
    }
}

# Remover pasta de backup grande
$pastaBackup = "backup_sistema_completo_20251025_071323"
if (Test-Path $pastaBackup) {
    try {
        Write-Host "  ⏳ Removendo pasta grande: $pastaBackup (pode demorar)..." -ForegroundColor Yellow
        Remove-Item $pastaBackup -Recurse -Force
        Write-Host "  ✓ Removida: $pastaBackup" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Erro ao remover $pastaBackup : $_" -ForegroundColor Red
        $erros++
    }
} else {
    Write-Host "  ⊘ Não encontrada: $pastaBackup" -ForegroundColor Gray
}

# =========================================
# Fase 3: Arquivar documentação histórica
# =========================================
Write-Host "`n📦 Fase 3: Arquivando documentação histórica..." -ForegroundColor Cyan

$docsArquivar = @(
    "ESTRATEGIA_ORGANIZACAO.md",
    "LIMPEZA_LOG_20251023.md",
    "RESUMO_LIMPEZA.md",
    "liberar_firewall.bat",
    "limpar_projeto.ps1"
)

foreach ($doc in $docsArquivar) {
    if (Test-Path $doc) {
        try {
            Move-Item $doc "docs\archived\" -Force
            Write-Host "  ✓ Arquivado: $doc" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao arquivar $doc : $_" -ForegroundColor Red
            $erros++
        }
    } else {
        Write-Host "  ⊘ Não encontrado: $doc" -ForegroundColor Gray
    }
}

# =========================================
# Fase 4: Organizar scripts
# =========================================
Write-Host "`n📜 Fase 4: Organizando scripts..." -ForegroundColor Cyan

# Scripts de análise
$scriptsAnalise = @(
    "analise_demanda_habilidades.py",
    "analise_scores.py"
)
foreach ($script in $scriptsAnalise) {
    if (Test-Path $script) {
        try {
            Move-Item $script "scripts\analise\" -Force
            Write-Host "  ✓ Movido para analise/: $script" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao mover $script : $_" -ForegroundColor Red
            $erros++
        }
    }
}

# Scripts de debug
$scriptsDebug = @(
    "check_db_contents.py",
    "check_schema.py",
    "check_table_structure.py",
    "debug_tabelas.py",
    "debug_table.py",
    "verificar_banco_completo.py",
    "verificar_banco.py",
    "verificar_profissionais.py",
    "verificar_sistema_demo.py",
    "verificar_tabelas.py"
)
foreach ($script in $scriptsDebug) {
    if (Test-Path $script) {
        try {
            Move-Item $script "scripts\debug\" -Force
            Write-Host "  ✓ Movido para debug/: $script" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao mover $script : $_" -ForegroundColor Red
            $erros++
        }
    }
}

# Scripts de população
$scriptsPopulacao = @(
    "popular_candidaturas.py",
    "popular_dados.py",
    "popular_profissionais_completo.py",
    "simulador_dados.py"
)
foreach ($script in $scriptsPopulacao) {
    if (Test-Path $script) {
        try {
            Move-Item $script "scripts\populacao\" -Force
            Write-Host "  ✓ Movido para populacao/: $script" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao mover $script : $_" -ForegroundColor Red
            $erros++
        }
    }
}

# Scripts de demo
if (Test-Path "preparar_demo.py") {
    try {
        Move-Item "preparar_demo.py" "scripts\demo\" -Force
        Write-Host "  ✓ Movido para demo/: preparar_demo.py" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Erro ao mover preparar_demo.py: $_" -ForegroundColor Red
        $erros++
    }
}

# Scripts de migração
if (Test-Path "update_schema.py") {
    try {
        Move-Item "update_schema.py" "scripts\migrations\" -Force
        Write-Host "  ✓ Movido para migrations/: update_schema.py" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Erro ao mover update_schema.py: $_" -ForegroundColor Red
        $erros++
    }
}

# Remover scripts de teste específicos
$scriptsRemoverEspecificos = @(
    "buscar_olivia.py",
    "enriquecer_perfil_maria.py"
)
foreach ($script in $scriptsRemoverEspecificos) {
    if (Test-Path $script) {
        try {
            Remove-Item $script -Force
            Write-Host "  ✓ Removido (específico): $script" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao remover $script : $_" -ForegroundColor Red
            $erros++
        }
    }
}

# =========================================
# Fase 5: Organizar testes
# =========================================
Write-Host "`n🧪 Fase 5: Organizando testes..." -ForegroundColor Cyan

$arquivosTeste = @(
    "teste_auth.py",
    "teste_dashboard_empresa.py",
    "teste_dashboard_profissional.py",
    "teste_dashboard_v1.4.py",
    "teste_fluxo_completo.py",
    "teste_init_banco.py",
    "teste_storytelling_completo.py",
    "testar_api_vagas.py",
    "testar_integracao_receita.py",
    "test_hash.py"
)

foreach ($teste in $arquivosTeste) {
    if (Test-Path $teste) {
        try {
            Move-Item $teste "tests\" -Force
            Write-Host "  ✓ Movido para tests/: $teste" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Erro ao mover $teste : $_" -ForegroundColor Red
            $erros++
        }
    }
}

# Mover teste frontend
if (Test-Path "test_cadastro.js") {
    try {
        Move-Item "test_cadastro.js" "tests\frontend\" -Force
        Write-Host "  ✓ Movido para tests/frontend/: test_cadastro.js" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Erro ao mover test_cadastro.js: $_" -ForegroundColor Red
        $erros++
    }
}

# =========================================
# Fase 6: Limpar cache Python
# =========================================
Write-Host "`n🧹 Fase 6: Limpando cache Python..." -ForegroundColor Cyan

try {
    $pycacheFolders = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
    $count = 0
    foreach ($folder in $pycacheFolders) {
        Remove-Item $folder.FullName -Recurse -Force
        $count++
    }
    Write-Host "  ✓ Removidas $count pastas __pycache__" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Erro ao limpar __pycache__: $_" -ForegroundColor Yellow
    $avisos++
}

try {
    $pycFiles = Get-ChildItem -Path . -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue
    $count = 0
    foreach ($file in $pycFiles) {
        Remove-Item $file.FullName -Force
        $count++
    }
    Write-Host "  ✓ Removidos $count arquivos .pyc" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Erro ao limpar .pyc: $_" -ForegroundColor Yellow
    $avisos++
}

# =========================================
# Relatório Final
# =========================================
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "✅ LIMPEZA CONCLUÍDA!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan

if ($erros -eq 0 -and $avisos -eq 0) {
    Write-Host "`n✨ Tudo foi executado perfeitamente!" -ForegroundColor Green
} else {
    Write-Host "`n📊 Resumo:" -ForegroundColor Yellow
    if ($erros -gt 0) {
        Write-Host "  ❌ Erros: $erros" -ForegroundColor Red
    }
    if ($avisos -gt 0) {
        Write-Host "  ⚠️  Avisos: $avisos" -ForegroundColor Yellow
    }
}

Write-Host "`n🔍 Próximos passos recomendados:" -ForegroundColor Cyan
Write-Host "  1. Verificar se o sistema inicia: py start_api.py" -ForegroundColor White
Write-Host "  2. Executar testes: cd tests && py teste_fluxo_completo.py" -ForegroundColor White
Write-Host "  3. Verificar git status: git status" -ForegroundColor White
Write-Host "  4. Fazer commit: git add . && git commit -m 'refactor: organize project structure'" -ForegroundColor White
Write-Host ""
