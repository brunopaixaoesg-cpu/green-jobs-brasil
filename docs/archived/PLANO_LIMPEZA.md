# 🧹 Plano de Limpeza - Green Jobs Brasil
**Data:** 01/11/2025  
**Objetivo:** Remover arquivos desnecessários e organizar estrutura do projeto

## 📊 Análise da Situação Atual

### Backups Compactados (Remover)
```
✗ backup_v1.2_20251016_205417.zip        (~5MB)
✗ backup_v1.3_auth_20251016_220802.zip   (~5MB)
✗ backup_v1.4_20251017_170723.rar        (~5MB)
```
**Justificativa:** Git é nosso controle de versão. Backups locais não são necessários.

### Pasta de Backup Descompactada (Remover)
```
✗ backup_sistema_completo_20251025_071323/  (107+ arquivos)
```
**Justificativa:** Duplica toda a estrutura do projeto. Git mantém histórico completo.

### Arquivos de Documentação Duplicados/Obsoletos (Consolidar)
```
✓ README.md                           → MANTER (versão principal atualizada)
✗ README_OLD.md                       → REMOVER
✗ README_BACKUP.md (na pasta backup)  → REMOVER
✓ DOCUMENTACAO_COMPLETA_v1.4.md       → MANTER (versão mais recente)
✗ DOCUMENTACAO_COMPLETA.md            → REMOVER (versão antiga)
✓ ROADMAP.md                          → MANTER (atualizado hoje)
✓ MAPA_ROTAS.md                       → MANTER
✓ COMO_USAR.md                        → MANTER
✗ ESTRATEGIA_ORGANIZACAO.md           → ARQUIVAR (informações já aplicadas)
✗ LIMPEZA_LOG_20251023.md             → ARQUIVAR (registro histórico)
✗ RESUMO_LIMPEZA.md                   → ARQUIVAR
✗ STATUS_FINAL_PROJETO.md             → REMOVER (info no README)
✗ SISTEMA_FUNCIONANDO.md              → REMOVER (info no README)
✗ SISTEMA_COMPLETO_FINAL.md           → REMOVER (info no README)
```

### Guias Específicos (Revisar)
```
✓ AUDITORIA_MOBILE_UX.md              → MANTER (referência futura)
✓ AUTENTICACAO_v1.3.md                → MANTER
✓ DASHBOARD_EMPRESA_v1.5.md           → MANTER
✓ DASHBOARD_PROFISSIONAL_v1.4.md      → MANTER
✓ DEPLOY_PASSO_A_PASSO.md             → MANTER
✓ GUIA_DEPLOY_MOBILE.md               → MANTER
✓ GUIA_DEPLOY_RENDER.md               → MANTER
✓ GUIA_INICIALIZACAO_DEMO.md          → MANTER
✓ GUIA_USUARIO_BRUNO.md               → MANTER
✓ MOBILE_FIRST_UX_v1.0.md             → MANTER
✓ ML_DASHBOARD_RESTAURADO.md          → MANTER
✓ STORYTELLING_v1.6_COMPLETO.md       → MANTER
```

### Scripts de Debug/Teste na Raiz (Organizar)
```
✗ analise_demanda_habilidades.py      → MOVER para scripts/analise/
✗ analise_scores.py                   → MOVER para scripts/analise/
✗ buscar_olivia.py                    → REMOVER (teste específico)
✗ check_db_contents.py                → MOVER para scripts/debug/
✗ check_schema.py                     → MOVER para scripts/debug/
✗ check_table_structure.py            → MOVER para scripts/debug/
✗ debug_tabelas.py                    → MOVER para scripts/debug/
✗ debug_table.py                      → MOVER para scripts/debug/
✗ enriquecer_perfil_maria.py          → REMOVER (teste específico)
✗ popular_candidaturas.py             → MOVER para scripts/populacao/
✗ popular_dados.py                    → MOVER para scripts/populacao/
✗ popular_profissionais_completo.py   → MOVER para scripts/populacao/
✗ preparar_demo.py                    → MOVER para scripts/demo/
✗ simulador_dados.py                  → MOVER para scripts/populacao/
✗ update_schema.py                    → MOVER para scripts/migrations/
✗ verificar_banco_completo.py         → MOVER para scripts/debug/
✗ verificar_banco.py                  → MOVER para scripts/debug/
✗ verificar_profissionais.py          → MOVER para scripts/debug/
✗ verificar_sistema_demo.py           → MOVER para scripts/debug/
✗ verificar_tabelas.py                → MOVER para scripts/debug/
```

### Scripts de Teste na Raiz (Organizar)
```
✗ teste_auth.py                       → MOVER para tests/
✗ teste_dashboard_empresa.py          → MOVER para tests/
✗ teste_dashboard_profissional.py     → MOVER para tests/
✗ teste_dashboard_v1.4.py             → MOVER para tests/
✗ teste_fluxo_completo.py             → MOVER para tests/
✗ teste_init_banco.py                 → MOVER para tests/
✗ teste_storytelling_completo.py      → MOVER para tests/
✗ testar_api_vagas.py                 → MOVER para tests/
✗ testar_integracao_receita.py        → MOVER para tests/
```

### Arquivos de Teste JavaScript/HTML
```
✗ test_cadastro.js                    → MOVER para tests/frontend/
✗ test_hash.py                        → MOVER para tests/
```

### Arquivos de Configuração/Utilitários
```
✓ INICIAR_DEMO.bat                    → MANTER
✓ INICIAR_SISTEMA.bat                 → MANTER
✓ TESTAR_SISTEMA.bat                  → MANTER
✗ liberar_firewall.bat                → ARQUIVAR (não essencial)
✗ limpar_projeto.ps1                  → REMOVER (substituir por este plano)
✓ requirements.txt                    → MANTER
✓ start_all.py                        → MANTER
✓ start_api.py                        → MANTER
```

## 🎯 Plano de Ação Detalhado

### Fase 1: Criar Estrutura de Pastas (Se não existir)
```powershell
# Criar subpastas para organização
New-Item -ItemType Directory -Path "scripts\analise" -Force
New-Item -ItemType Directory -Path "scripts\debug" -Force
New-Item -ItemType Directory -Path "scripts\demo" -Force
New-Item -ItemType Directory -Path "scripts\migrations" -Force
New-Item -ItemType Directory -Path "scripts\populacao" -Force
New-Item -ItemType Directory -Path "tests\frontend" -Force
New-Item -ItemType Directory -Path "docs\archived" -Force
```

### Fase 2: Remover Backups e Duplicatas (SEGURO - Git tem histórico)
```powershell
# Backups compactados
Remove-Item "backup_v1.2_20251016_205417.zip" -Force
Remove-Item "backup_v1.3_auth_20251016_220802.zip" -Force
Remove-Item "backup_v1.4_20251017_170723.rar" -Force

# Pasta de backup completa
Remove-Item "backup_sistema_completo_20251025_071323" -Recurse -Force

# README duplicado
Remove-Item "README_OLD.md" -Force

# Documentação obsoleta (versões antigas)
Remove-Item "DOCUMENTACAO_COMPLETA.md" -Force
Remove-Item "STATUS_FINAL_PROJETO.md" -Force
Remove-Item "SISTEMA_FUNCIONANDO.md" -Force
Remove-Item "SISTEMA_COMPLETO_FINAL.md" -Force
```

### Fase 3: Arquivar Documentação Histórica
```powershell
# Mover documentos de planejamento/log para arquivo
Move-Item "ESTRATEGIA_ORGANIZACAO.md" "docs\archived\" -Force
Move-Item "LIMPEZA_LOG_20251023.md" "docs\archived\" -Force
Move-Item "RESUMO_LIMPEZA.md" "docs\archived\" -Force
Move-Item "liberar_firewall.bat" "docs\archived\" -Force
Move-Item "limpar_projeto.ps1" "docs\archived\" -Force
```

### Fase 4: Organizar Scripts (Mover para Subpastas)
```powershell
# Scripts de análise
Move-Item "analise_demanda_habilidades.py" "scripts\analise\" -Force
Move-Item "analise_scores.py" "scripts\analise\" -Force

# Scripts de debug
Move-Item "check_db_contents.py" "scripts\debug\" -Force
Move-Item "check_schema.py" "scripts\debug\" -Force
Move-Item "check_table_structure.py" "scripts\debug\" -Force
Move-Item "debug_tabelas.py" "scripts\debug\" -Force
Move-Item "debug_table.py" "scripts\debug\" -Force
Move-Item "verificar_banco_completo.py" "scripts\debug\" -Force
Move-Item "verificar_banco.py" "scripts\debug\" -Force
Move-Item "verificar_profissionais.py" "scripts\debug\" -Force
Move-Item "verificar_sistema_demo.py" "scripts\debug\" -Force
Move-Item "verificar_tabelas.py" "scripts\debug\" -Force

# Scripts de população
Move-Item "popular_candidaturas.py" "scripts\populacao\" -Force
Move-Item "popular_dados.py" "scripts\populacao\" -Force
Move-Item "popular_profissionais_completo.py" "scripts\populacao\" -Force
Move-Item "simulador_dados.py" "scripts\populacao\" -Force

# Scripts de demo
Move-Item "preparar_demo.py" "scripts\demo\" -Force

# Scripts de migração
Move-Item "update_schema.py" "scripts\migrations\" -Force

# Remover scripts de teste específicos
Remove-Item "buscar_olivia.py" -Force
Remove-Item "enriquecer_perfil_maria.py" -Force
```

### Fase 5: Organizar Testes
```powershell
# Mover testes Python para tests/
Move-Item "teste_auth.py" "tests\" -Force
Move-Item "teste_dashboard_empresa.py" "tests\" -Force
Move-Item "teste_dashboard_profissional.py" "tests\" -Force
Move-Item "teste_dashboard_v1.4.py" "tests\" -Force
Move-Item "teste_fluxo_completo.py" "tests\" -Force
Move-Item "teste_init_banco.py" "tests\" -Force
Move-Item "teste_storytelling_completo.py" "tests\" -Force
Move-Item "testar_api_vagas.py" "tests\" -Force
Move-Item "testar_integracao_receita.py" "tests\" -Force
Move-Item "test_hash.py" "tests\" -Force

# Mover testes frontend
Move-Item "test_cadastro.js" "tests\frontend\" -Force
```

### Fase 6: Limpar Cache Python
```powershell
# Remover todos os __pycache__
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remover arquivos .pyc soltos
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

## 📋 Estrutura Final Esperada

```
C:\Users\Bruno\Empresas Verdes\
│
├── 📄 Core
│   ├── README.md
│   ├── ROADMAP.md
│   ├── requirements.txt
│   ├── start_api.py
│   ├── start_all.py
│   └── gjb_dev.db
│
├── 🔌 api/
│   ├── app.py
│   ├── main.py
│   ├── sqlite_api_clean.py
│   ├── db.py
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── 📚 Documentação
│   ├── COMO_USAR.md
│   ├── MAPA_ROTAS.md
│   ├── DOCUMENTACAO_COMPLETA_v1.4.md
│   ├── AUTENTICACAO_v1.3.md
│   ├── DASHBOARD_EMPRESA_v1.5.md
│   ├── DASHBOARD_PROFISSIONAL_v1.4.md
│   ├── STORYTELLING_v1.6_COMPLETO.md
│   ├── DEPLOY_PASSO_A_PASSO.md
│   ├── GUIA_DEPLOY_MOBILE.md
│   ├── GUIA_DEPLOY_RENDER.md
│   ├── GUIA_INICIALIZACAO_DEMO.md
│   ├── GUIA_USUARIO_BRUNO.md
│   ├── MOBILE_FIRST_UX_v1.0.md
│   ├── ML_DASHBOARD_RESTAURADO.md
│   └── AUDITORIA_MOBILE_UX.md
│
├── 🧪 tests/
│   ├── teste_*.py
│   ├── testar_*.py
│   └── frontend/
│       └── test_cadastro.js
│
├── 📜 scripts/
│   ├── analise/
│   ├── debug/
│   ├── demo/
│   ├── migrations/
│   └── populacao/
│
├── 🗄️ data/
├── 🗄️ db/
├── 🔄 etl/
├── 🤖 ml/
│
├── 🚀 Launchers
│   ├── INICIAR_SISTEMA.bat
│   ├── INICIAR_DEMO.bat
│   └── TESTAR_SISTEMA.bat
│
└── 📁 docs/archived/
    └── (documentos históricos)
```

## 🚀 Script de Execução Completo

Salvar como `executar_limpeza.ps1` e executar:

```powershell
# Script de limpeza completo - Green Jobs Brasil
Write-Host "🧹 Iniciando limpeza do projeto..." -ForegroundColor Green

# Fase 1: Criar estrutura
Write-Host "`n📁 Fase 1: Criando estrutura de pastas..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "scripts\analise" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts\debug" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts\demo" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts\migrations" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts\populacao" -Force | Out-Null
New-Item -ItemType Directory -Path "tests\frontend" -Force | Out-Null
New-Item -ItemType Directory -Path "docs\archived" -Force | Out-Null

# Fase 2: Remover backups
Write-Host "`n🗑️ Fase 2: Removendo backups..." -ForegroundColor Cyan
Remove-Item "backup_v1.2_20251016_205417.zip" -Force -ErrorAction SilentlyContinue
Remove-Item "backup_v1.3_auth_20251016_220802.zip" -Force -ErrorAction SilentlyContinue
Remove-Item "backup_v1.4_20251017_170723.rar" -Force -ErrorAction SilentlyContinue
Remove-Item "backup_sistema_completo_20251025_071323" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "README_OLD.md" -Force -ErrorAction SilentlyContinue
Remove-Item "DOCUMENTACAO_COMPLETA.md" -Force -ErrorAction SilentlyContinue
Remove-Item "STATUS_FINAL_PROJETO.md" -Force -ErrorAction SilentlyContinue
Remove-Item "SISTEMA_FUNCIONANDO.md" -Force -ErrorAction SilentlyContinue
Remove-Item "SISTEMA_COMPLETO_FINAL.md" -Force -ErrorAction SilentlyContinue

# Fase 3: Arquivar documentação histórica
Write-Host "`n📦 Fase 3: Arquivando documentação histórica..." -ForegroundColor Cyan
Move-Item "ESTRATEGIA_ORGANIZACAO.md" "docs\archived\" -Force -ErrorAction SilentlyContinue
Move-Item "LIMPEZA_LOG_20251023.md" "docs\archived\" -Force -ErrorAction SilentlyContinue
Move-Item "RESUMO_LIMPEZA.md" "docs\archived\" -Force -ErrorAction SilentlyContinue
Move-Item "liberar_firewall.bat" "docs\archived\" -Force -ErrorAction SilentlyContinue
Move-Item "limpar_projeto.ps1" "docs\archived\" -Force -ErrorAction SilentlyContinue

# Fase 4: Organizar scripts
Write-Host "`n📜 Fase 4: Organizando scripts..." -ForegroundColor Cyan
# Análise
Move-Item "analise_demanda_habilidades.py" "scripts\analise\" -Force -ErrorAction SilentlyContinue
Move-Item "analise_scores.py" "scripts\analise\" -Force -ErrorAction SilentlyContinue
# Debug
$debugFiles = @("check_db_contents.py", "check_schema.py", "check_table_structure.py", 
                "debug_tabelas.py", "debug_table.py", "verificar_banco_completo.py",
                "verificar_banco.py", "verificar_profissionais.py", "verificar_sistema_demo.py", 
                "verificar_tabelas.py")
foreach ($file in $debugFiles) {
    Move-Item $file "scripts\debug\" -Force -ErrorAction SilentlyContinue
}
# População
$popFiles = @("popular_candidaturas.py", "popular_dados.py", 
              "popular_profissionais_completo.py", "simulador_dados.py")
foreach ($file in $popFiles) {
    Move-Item $file "scripts\populacao\" -Force -ErrorAction SilentlyContinue
}
# Demo e migrações
Move-Item "preparar_demo.py" "scripts\demo\" -Force -ErrorAction SilentlyContinue
Move-Item "update_schema.py" "scripts\migrations\" -Force -ErrorAction SilentlyContinue
# Remover scripts específicos
Remove-Item "buscar_olivia.py" -Force -ErrorAction SilentlyContinue
Remove-Item "enriquecer_perfil_maria.py" -Force -ErrorAction SilentlyContinue

# Fase 5: Organizar testes
Write-Host "`n🧪 Fase 5: Organizando testes..." -ForegroundColor Cyan
$testFiles = @("teste_auth.py", "teste_dashboard_empresa.py", "teste_dashboard_profissional.py",
               "teste_dashboard_v1.4.py", "teste_fluxo_completo.py", "teste_init_banco.py",
               "teste_storytelling_completo.py", "testar_api_vagas.py", 
               "testar_integracao_receita.py", "test_hash.py")
foreach ($file in $testFiles) {
    Move-Item $file "tests\" -Force -ErrorAction SilentlyContinue
}
Move-Item "test_cadastro.js" "tests\frontend\" -Force -ErrorAction SilentlyContinue

# Fase 6: Limpar cache
Write-Host "`n🧹 Fase 6: Limpando cache Python..." -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "`n✅ Limpeza concluída com sucesso!" -ForegroundColor Green
Write-Host "📊 Verifique a nova estrutura e teste o sistema." -ForegroundColor Yellow
```

## 📊 Resultados Esperados

### Antes da Limpeza
- **Arquivos na raiz:** ~80 arquivos
- **Tamanho total:** ~50MB (com backups)
- **Organização:** Caótica

### Depois da Limpeza
- **Arquivos na raiz:** ~15 arquivos essenciais
- **Tamanho total:** ~25MB
- **Organização:** Estruturada e clara

## ✅ Checklist de Validação

Após executar a limpeza, verificar:

- [ ] Sistema inicia corretamente: `py start_api.py`
- [ ] API responde: http://127.0.0.1:8002/
- [ ] Documentação acessível no repositório
- [ ] Testes executam: `cd tests && py teste_fluxo_completo.py`
- [ ] Banco de dados intacto: `gjb_dev.db` presente
- [ ] Git status limpo (nenhum arquivo crítico removido por engano)

## 🎯 Próximos Passos (Após Limpeza)

1. **Commit da limpeza:** `git add . && git commit -m "refactor: organize project structure and remove duplicates"`
2. **Retomar roadmap:** Seguir prioridades definidas em ROADMAP.md
3. **Focar no MVP:** Storytelling UX, filtros avançados, preparação deploy

---

**Status:** Pronto para execução  
**Reversível:** Sim (via Git)  
**Seguro:** Sim (apenas duplicatas e backups)
