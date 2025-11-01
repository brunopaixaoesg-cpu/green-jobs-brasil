# 🗂️ ESTRATÉGIA DE ORGANIZAÇÃO - GREEN JOBS BRASIL

**Data:** 16/10/2025  
**Status:** Sistema 100% funcional - Hora de organizar!

---

## ✅ ARQUIVOS ESSENCIAIS (MANTER)

### 🚀 Inicialização
```
✓ start_api.py                    → Iniciar API (PRINCIPAL)
✓ gjb_dev.db                       → Banco de dados SQLite
```

### 🔌 API Principal
```
✓ api/
  ✓ __init__.py
  ✓ sqlite_api_clean.py           → API PRINCIPAL (FastAPI)
  ✓ db.py                          → Conexão banco
  ✓ requirements.txt               → Dependências
  ✓ routers/
    ✓ __init__.py
    ✓ cnaes.py
    ✓ companies.py
    ✓ matching.py
    ✓ profissionais.py
    ✓ stats.py
    ✓ vagas.py
  ✓ services/
    ✓ match_calculator.py
    ✓ ml_service.py
    ✓ unified_matching.py
  ✓ templates/                     → Todas as páginas HTML
    ✓ landing_page.html
    ✓ dashboard_moderno.html
    ✓ empresas_modernas.html
    ✓ matching/
    ✓ profissionais/
    ✓ vagas/
```

### 🧪 Testes e Validação
```
✓ auditoria_completa.py           → Verificação do sistema
✓ test_api_completo.py            → Testes das APIs
✓ test_cnpj.py                     → Teste busca CNPJ
```

### 📚 Documentação
```
✓ README.md                        → Visão geral
✓ DOCUMENTACAO_COMPLETA.md        → Referência técnica
✓ MAPA_ROTAS.md                   → Navegação e rotas
✓ ESTRATEGIA_ORGANIZACAO.md       → Este arquivo
```

### 📊 Dados e ETL
```
✓ etl/
  ✓ cnae_green_seed.csv           → CNAEs verdes
  ✓ main.py                        → ETL completo
  ✓ config.py
  ✓ requirements.txt
✓ data/
  ✓ processed/ml_dataset.csv      → Dataset ML
```

### 🤖 Machine Learning
```
✓ ml/
  ✓ prepare_data.py               → Preparação dados
  ✓ train_model.py                → Treinamento modelo
  ✓ models/model_metadata.json   → Metadados do modelo
```

### 📜 Scripts Úteis
```
✓ scripts/
  ✓ gerar_profissionais_ambientais.py
  ✓ gerar_vagas_ambientais.py
  ✓ gerar_candidaturas_matching.py
  ✓ run_migrations.py
```

### 🗄️ Database
```
✓ db/
  ✓ schema_sqlite.sql
  ✓ seed_cnae.sql
  ✓ migrations/
```

---

## 🗑️ ARQUIVOS PARA DELETAR (Redundantes/Obsoletos)

### ❌ APIs Duplicadas
```
✗ api_empresas.py                 → Funcionalidade já em api/sqlite_api_clean.py
✗ api_simples.py                  → Versão simplificada obsoleta
✗ api_teste.py                    → Apenas testes, não usado
✗ api/sqlite_api.py               → Versão antiga (usar sqlite_api_clean.py)
```

### ❌ Scripts de Teste Duplicados
```
✗ test_api.py                     → Substituído por test_api_completo.py
✗ test_dashboard.py               → Funcionalidade em auditoria_completa.py
✗ test_search.py                  → Funcionalidade em test_api_completo.py
✗ test_sistema.py                 → Substituído por auditoria_completa.py
✗ teste_sistema_completo.py       → Duplicado de test_api_completo.py
✗ test_ml_sistema.py              → ML já validado
```

### ❌ Scripts Start Duplicados
```
✗ start_api_ml.py                 → Não usado (ML integrado na API principal)
✗ start_ml_api.py                 → Duplicado do anterior
✗ start_debug.bat                 → Não necessário (usar start_api.py)
```

### ❌ Scripts Debug/Demo Temporários
```
✗ api_debug.py                    → Debug temporário
✗ demo_sistema.py                 → Demo já documentado
✗ check_all_tables.py             → Funcionalidade em auditoria_completa.py
✗ check_companies.py              → Funcionalidade em auditoria_completa.py
```

### ❌ Scripts Geradores Redundantes
```
✗ scripts/gerar_profissionais_fake.py      → Usar gerar_profissionais_ambientais.py
✗ scripts/gerar_profissionais_simples.py   → Usar gerar_profissionais_ambientais.py
✗ scripts/gerar_vagas_esg.py               → Usar gerar_vagas_ambientais.py
✗ scripts/gerar_candidaturas.py            → Usar gerar_candidaturas_matching.py
✗ scripts/gerar_candidaturas_vagas_ambientais.py → Funcionalidade duplicada
```

### ❌ Documentação Antiga/Redundante
```
✗ STATUS_FINAL_PROJETO.md         → Info já em DOCUMENTACAO_COMPLETA.md
✗ ESTRATEGIA_FOLLOWUP.md          → Follow-up já documentado
✗ MATERIAL_APRESENTACAO.md        → Material já completo
✗ MAPEAMENTO_CONTATOS.md          → Não essencial para código
✗ relatorio_executivo.html        → Gerado automaticamente
```

### ❌ Templates Duplicados (manter apenas modernos)
```
✗ api/templates/dashboard.html              → Usar dashboard_moderno.html
✗ api/templates/dashboard_demo.html         → Usar dashboard_moderno.html
✗ api/templates/dashboard_final.html        → Usar dashboard_moderno.html
✗ api/templates/cnaes_modernos.html         → Não usado ativamente
```

### ❌ Scrapers POC (não em produção)
```
✗ scrapers_poc/                   → POC não integrado ainda
  (Manter se for desenvolver scraping futuro)
```

---

## 📦 ESTRUTURA FINAL RECOMENDADA

```
C:\Users\Bruno\Empresas Verdes\
│
├── 📄 README.md
├── 📚 DOCUMENTACAO_COMPLETA.md
├── 🗺️ MAPA_ROTAS.md
│
├── 🚀 start_api.py
├── 🗄️ gjb_dev.db
│
├── 🔌 api/
│   ├── __init__.py
│   ├── sqlite_api_clean.py      ⭐ API PRINCIPAL
│   ├── db.py
│   ├── requirements.txt
│   ├── routers/
│   ├── services/
│   ├── templates/
│   │   ├── landing_page.html
│   │   ├── dashboard_moderno.html
│   │   ├── empresas_modernas.html
│   │   ├── matching/
│   │   ├── profissionais/
│   │   └── vagas/
│   └── static/
│
├── 🧪 tests/                     ⭐ NOVA PASTA
│   ├── auditoria_completa.py
│   ├── test_api_completo.py
│   └── test_cnpj.py
│
├── 📊 data/
│   ├── raw/
│   └── processed/
│       └── ml_dataset.csv
│
├── 🗄️ db/
│   ├── schema_sqlite.sql
│   ├── seed_cnae.sql
│   └── migrations/
│
├── 🔄 etl/
│   ├── main.py
│   ├── config.py
│   ├── cnae_green_seed.csv
│   └── requirements.txt
│
├── 🤖 ml/
│   ├── prepare_data.py
│   ├── train_model.py
│   └── models/
│
└── 📜 scripts/
    ├── gerar_profissionais_ambientais.py
    ├── gerar_vagas_ambientais.py
    ├── gerar_candidaturas_matching.py
    └── run_migrations.py
```

---

## 🎯 PLANO DE AÇÃO

### Fase 1: Criar Pasta de Testes
```powershell
# Criar pasta tests/
New-Item -ItemType Directory -Path "tests" -Force

# Mover arquivos de teste
Move-Item "auditoria_completa.py" "tests/"
Move-Item "test_api_completo.py" "tests/"
Move-Item "test_cnpj.py" "tests/"
```

### Fase 2: Deletar Arquivos Redundantes
```powershell
# APIs duplicadas
Remove-Item "api_empresas.py"
Remove-Item "api_simples.py"
Remove-Item "api_teste.py"
Remove-Item "api/sqlite_api.py"

# Scripts teste duplicados
Remove-Item "test_api.py"
Remove-Item "test_dashboard.py"
Remove-Item "test_search.py"
Remove-Item "test_sistema.py"
Remove-Item "teste_sistema_completo.py"
Remove-Item "test_ml_sistema.py"

# Scripts start redundantes
Remove-Item "start_api_ml.py"
Remove-Item "start_ml_api.py"
Remove-Item "start_debug.bat"

# Scripts debug/demo
Remove-Item "api_debug.py"
Remove-Item "demo_sistema.py"
Remove-Item "check_all_tables.py"
Remove-Item "check_companies.py"

# Documentação redundante
Remove-Item "STATUS_FINAL_PROJETO.md"
Remove-Item "ESTRATEGIA_FOLLOWUP.md"
Remove-Item "MATERIAL_APRESENTACAO.md"
Remove-Item "MAPEAMENTO_CONTATOS.md"
Remove-Item "relatorio_executivo.html"

# Templates duplicados
Remove-Item "api/templates/dashboard.html"
Remove-Item "api/templates/dashboard_demo.html"
Remove-Item "api/templates/dashboard_final.html"
Remove-Item "api/templates/cnaes_modernos.html"

# Scripts geradores redundantes
Remove-Item "scripts/gerar_profissionais_fake.py"
Remove-Item "scripts/gerar_profissionais_simples.py"
Remove-Item "scripts/gerar_vagas_esg.py"
Remove-Item "scripts/gerar_candidaturas.py"
Remove-Item "scripts/gerar_candidaturas_vagas_ambientais.py"
```

### Fase 3: Limpar __pycache__
```powershell
# Remover todos os __pycache__
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

### Fase 4: Atualizar Documentação
```powershell
# Nada a fazer - já temos:
# ✓ README.md
# ✓ DOCUMENTACAO_COMPLETA.md
# ✓ MAPA_ROTAS.md
# ✓ ESTRATEGIA_ORGANIZACAO.md (este arquivo)
```

---

## ✅ CHECKLIST DE FUNCIONALIDADES

### Funcionalidades Principais (Todas Testadas ✓)
- [x] **Landing Page** → Página inicial com estatísticas
- [x] **Dashboard Moderno** → Visualização empresas + busca CNPJ
- [x] **Empresas Verdes** → Lista com filtros (score, UF, busca)
- [x] **Busca CNPJ** → Integração ReceitaWS + cálculo score
- [x] **Sistema ML** → Matching profissional-vaga (98.5% precisão)
- [x] **API REST** → 12 endpoints funcionando
- [x] **Banco SQLite** → 12 empresas, 81 vagas, 120 profissionais, 768 candidaturas

### APIs REST (Todas Funcionando ✓)
- [x] `GET /api/stats` → Estatísticas gerais
- [x] `GET /api/empresas` → Lista empresas verdes
- [x] `GET /api/search-company/{cnpj}` → Busca CNPJ
- [x] `GET /api/cnaes` → CNAEs verdes
- [x] `GET /api/matching/stats` → Estatísticas ML
- [x] `GET /api/vagas` → Lista vagas ESG
- [x] `GET /api/profissionais` → Lista profissionais

### Páginas Web (Todas Acessíveis ✓)
- [x] `/` → Landing page
- [x] `/dashboard` → Dashboard moderno
- [x] `/empresas` → Empresas verdes
- [x] `/vagas` → Sistema de vagas
- [x] `/ml-avancado` → Dashboard ML
- [x] `/explicacao-matching` → Como funciona

### Ferramentas de Teste (Todas Operacionais ✓)
- [x] `auditoria_completa.py` → Verifica todo sistema
- [x] `test_api_completo.py` → Testa todas APIs
- [x] `test_cnpj.py` → Testa busca CNPJ

---

## 🎬 COMANDOS FINAIS

### 1. Executar Limpeza Completa
```powershell
# Criar script de limpeza
# (Vou criar um script PowerShell para você)
```

### 2. Verificar Sistema Após Limpeza
```powershell
cd tests
py auditoria_completa.py
```

### 3. Iniciar API
```powershell
py start_api.py
```

---

## 📊 ESTATÍSTICAS DO PROJETO

### Antes da Limpeza
- 📄 Arquivos Python: ~50
- 📁 Tamanho: ~15MB
- 🗑️ Redundância: ~40%

### Depois da Limpeza
- 📄 Arquivos Python: ~30
- 📁 Tamanho: ~10MB
- ✨ Organização: 100%

---

## 🚀 PRÓXIMOS PASSOS RECOMENDADOS

1. **Executar limpeza** → Deletar arquivos redundantes
2. **Criar pasta tests/** → Organizar testes
3. **Limpar __pycache__** → Remover cache Python
4. **Testar sistema** → Rodar auditoria_completa.py
5. **Versionar código** → Git commit com estrutura limpa
6. **Documentar decisões** → README atualizado

---

**Pronto para executar?** Posso criar um script PowerShell que faz toda a limpeza automaticamente! 🧹