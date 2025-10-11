# 🏗️ Arquitetura Green Jobs Brasil

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Módulos e Responsabilidades](#módulos-e-responsabilidades)
4. [Fluxo de Dados](#fluxo-de-dados)
5. [Versionamento e Branches](#versionamento-e-branches)

---

## 🎯 Visão Geral

Green Jobs Brasil é uma plataforma modular para conectar empresas ESG com profissionais sustentáveis, através de classificação por ODS e matching inteligente.

### Princípios Arquiteturais:
- ✅ **Modular**: Cada funcionalidade em módulos independentes
- ✅ **Escalável**: Fácil adicionar novos recursos
- ✅ **Testável**: Código separado em camadas
- ✅ **Versionado**: Git com branches por feature
- ✅ **API-First**: Backend via FastAPI RESTful

---

## 📁 Estrutura de Pastas

```
C:\Users\Bruno\Empresas Verdes\
│
├── .git/                          # Controle de versão
├── .github/                       # Configurações GitHub
│   ├── copilot-instructions.md
│   └── workflows/
│
├── api/                           # 🌐 Backend FastAPI
│   ├── __init__.py
│   ├── sqlite_api.py             # ✅ API principal (ATUAL)
│   ├── models.py                 # Modelos SQLAlchemy
│   ├── schemas.py                # Schemas Pydantic
│   ├── db.py                     # Conexão banco
│   │
│   ├── routers/                  # 🔀 Endpoints organizados
│   │   ├── companies.py          # ✅ Rotas empresas
│   │   ├── cnaes.py              # ✅ Rotas CNAEs
│   │   ├── stats.py              # ✅ Estatísticas
│   │   ├── vagas.py              # 🆕 Rotas vagas (NOVO)
│   │   ├── profissionais.py      # 🆕 Rotas profissionais (NOVO)
│   │   └── matching.py           # 🆕 Algoritmo matching (NOVO)
│   │
│   ├── templates/                # 🎨 Frontend HTML
│   │   ├── dashboard_moderno.html    # ✅ Dashboard principal
│   │   ├── empresas_modernas.html    # ✅ Lista empresas
│   │   ├── cnaes_modernos.html       # ✅ Lista CNAEs
│   │   ├── vagas/                    # 🆕 Templates vagas (NOVO)
│   │   │   ├── lista.html
│   │   │   ├── criar.html
│   │   │   └── detalhes.html
│   │   └── profissionais/            # 🆕 Templates profissionais (NOVO)
│   │       ├── cadastro.html
│   │       ├── feed.html
│   │       └── perfil.html
│   │
│   └── static/                   # 📦 Arquivos estáticos
│       ├── Logo_GJB_SVG.svg
│       ├── css/
│       ├── js/
│       └── images/
│
├── etl/                          # 📊 ETL e Processamento de Dados
│   ├── main.py                   # ✅ Pipeline ETL principal
│   ├── real_data_processor.py    # ✅ Integração Receita Federal
│   ├── cnae_green_seed.csv       # ✅ CNAEs verdes classificados
│   ├── config.py                 # Configurações ETL
│   └── requirements.txt
│
├── db/                           # 🗄️ Schema e Seeds
│   ├── schema_sqlite.sql         # ✅ Schema atual
│   ├── migrations/               # 🆕 Migrações futuras (NOVO)
│   │   ├── 001_add_vagas.sql
│   │   └── 002_add_profissionais.sql
│   └── seed_cnae.sql             # ✅ Seed CNAEs verdes
│
├── data/                         # 📂 Dados brutos e processados
│   ├── raw/                      # Dados originais
│   └── processed/                # Dados processados
│
├── tests/                        # 🧪 Testes automatizados (FUTURO)
│   ├── test_api.py
│   ├── test_matching.py
│   └── test_etl.py
│
├── docs/                         # 📚 Documentação adicional
│   ├── API.md                    # Documentação API
│   ├── MATCHING.md               # Algoritmo de matching
│   └── ODS_MAPPING.md            # Mapeamento CNAEs-ODS
│
├── scripts/                      # 🛠️ Scripts utilitários
│   ├── import_leads.py           # Importar 3mil empresas
│   ├── backup_db.py              # Backup banco de dados
│   └── migrate.py                # Migrations
│
├── gjb_dev.db                    # ✅ Banco SQLite (desenvolvimento)
├── start_api.py                  # ✅ Iniciar API
├── requirements.txt              # 🆕 Dependências consolidadas (NOVO)
├── .env.example                  # Variáveis de ambiente exemplo
├── .gitignore                    # ✅ Arquivos ignorados Git
│
└── README.md                     # ✅ Documentação principal

```

---

## 🧩 Módulos e Responsabilidades

### **Módulo 1: Classificação de Empresas (✅ EXISTENTE)**
**Status:** Funcionando  
**Arquivos:**
- `api/sqlite_api.py` - API principal
- `api/routers/companies.py` - Endpoints empresas
- `api/routers/cnaes.py` - Endpoints CNAEs
- `etl/real_data_processor.py` - Busca dados Receita Federal

**Funcionalidades:**
- ✅ Classificar empresas por CNAE verde
- ✅ Calcular score sustentável (0-100)
- ✅ Mapear para ODS
- ✅ Dashboard visualização

---

### **Módulo 2: Sistema de Vagas ESG (🆕 EM DESENVOLVIMENTO)**
**Status:** A desenvolver  
**Arquivos:**
- `api/routers/vagas.py` - CRUD vagas
- `api/templates/vagas/*.html` - Frontend vagas
- `db/migrations/001_add_vagas.sql` - Tabela vagas

**Funcionalidades:**
- [ ] Empresas publicam vagas ESG
- [ ] Tags ODS por vaga
- [ ] Habilidades ESG requeridas
- [ ] Status vaga (ativa/pausada/fechada)

**Tabela:**
```sql
CREATE TABLE vagas_esg (
    id INTEGER PRIMARY KEY,
    cnpj TEXT REFERENCES empresas_verdes(cnpj),
    titulo TEXT NOT NULL,
    descricao TEXT,
    ods_tags TEXT, -- JSON [7, 13, 15]
    habilidades_requeridas TEXT, -- JSON
    nivel_experiencia TEXT,
    tipo_contratacao TEXT,
    localizacao TEXT,
    salario_min REAL,
    salario_max REAL,
    remoto BOOLEAN,
    status TEXT DEFAULT 'ativa',
    criada_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizada_em DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

---

### **Módulo 3: Perfil Profissional (🆕 EM DESENVOLVIMENTO)**
**Status:** A desenvolver  
**Arquivos:**
- `api/routers/profissionais.py` - CRUD profissionais
- `api/templates/profissionais/*.html` - Frontend
- `db/migrations/002_add_profissionais.sql` - Tabela profissionais

**Funcionalidades:**
- [ ] Cadastro profissional verde
- [ ] ODS de interesse
- [ ] Habilidades e certificações ESG
- [ ] Upload currículo

**Tabela:**
```sql
CREATE TABLE profissionais_esg (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    nome_completo TEXT,
    telefone TEXT,
    linkedin TEXT,
    ods_interesse TEXT, -- JSON
    habilidades_esg TEXT, -- JSON
    certificacoes TEXT, -- JSON
    anos_experiencia_esg INTEGER,
    formacao TEXT,
    localizacao_uf TEXT,
    aceita_remoto BOOLEAN,
    pretensao_salarial REAL,
    tipo_oportunidade TEXT,
    curriculo_url TEXT,
    status TEXT DEFAULT 'ativo',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

---

### **Módulo 4: Matching Inteligente (🆕 EM DESENVOLVIMENTO)**
**Status:** A desenvolver  
**Arquivos:**
- `api/routers/matching.py` - Algoritmo matching
- `api/services/match_calculator.py` - Cálculo score

**Funcionalidades:**
- [ ] Score de compatibilidade (0-100)
- [ ] Match ODS (40 pontos)
- [ ] Match habilidades (30 pontos)
- [ ] Match experiência (15 pontos)
- [ ] Match localização (10 pontos)
- [ ] Match salário (5 pontos)

**Endpoint:**
```
GET /api/matching/vaga/{vaga_id}/candidatos
→ Retorna top 50 profissionais com score > 60
```

---

### **Módulo 5: Importação de Leads (🆕 PLANEJADO)**
**Status:** Planejado  
**Arquivos:**
- `scripts/import_leads.py` - Script importação massa

**Funcionalidades:**
- [ ] Importar CSV com 3mil CNPJs
- [ ] Buscar dados na Receita Federal
- [ ] Calcular score verde
- [ ] Classificar por potencial
- [ ] Marcar como leads qualificados

---

## 🔄 Fluxo de Dados

### **1. Cadastro de Empresa**
```
CNPJ → Receita Federal API → 
Dados completos → Calcular Score Verde → 
Classificar CNAEs → Mapear ODS → 
Salvar DB (empresas_verdes)
```

### **2. Publicação de Vaga**
```
Empresa autenticada → Formulário vaga → 
Selecionar ODS tags → Definir habilidades → 
Salvar DB (vagas_esg) → 
Disparar matching automático
```

### **3. Cadastro Profissional**
```
Email/LinkedIn → Formulário perfil → 
Selecionar ODS interesse → Habilidades ESG → 
Upload currículo → Salvar DB (profissionais_esg) → 
Sugerir vagas compatíveis
```

### **4. Matching**
```
Nova vaga criada → 
Buscar profissionais ativos → 
Calcular score compatibilidade → 
Retornar top 50 matches → 
Notificar empresa + profissionais
```

---

## 🌿 Versionamento e Branches

### **Branch Strategy:**

#### **`master`** (ou `main`)
- ✅ Código estável e funcionando
- ✅ Deploy em produção
- 🔒 Protegida (só via Pull Request)

#### **`develop`**
- 🔨 Integração de features
- 🧪 Testes antes de merge para master
- 📦 Versões beta

#### **`feature/*`**
- 🆕 Novas funcionalidades
- Exemplos:
  - `feature/matching-system` ← **ATUAL**
  - `feature/auth-system`
  - `feature/payment-integration`

#### **`hotfix/*`**
- 🚨 Correções urgentes em produção
- Merge direto para master + develop

### **Workflow:**
```
1. Criar feature branch
   git checkout -b feature/nova-funcionalidade

2. Desenvolver e commitar
   git add .
   git commit -m "feat: descrição"

3. Testar localmente
   python test_api.py

4. Merge para develop
   git checkout develop
   git merge feature/nova-funcionalidade

5. Testar em develop

6. Merge para master (produção)
   git checkout master
   git merge develop
```

---

## 🔐 Segurança e Backup

### **Git:**
- ✅ Todo código versionado
- ✅ Histórico completo de mudanças
- ✅ Fácil reverter para versão anterior

### **Banco de Dados:**
- ⚠️ `gjb_dev.db` não versionado (muito grande)
- 📦 Fazer backup manual regular
- 🆕 Criar script `scripts/backup_db.py`

### **Variáveis Sensíveis:**
- 🔒 Nunca commitar senhas, tokens, chaves API
- ✅ Usar `.env` (ignorado pelo Git)
- 📝 `.env.example` como template

---

## 🚀 Próximos Passos

### **Imediato (esta semana):**
1. ✅ Git e backup configurados
2. 🆕 Desenvolver Módulo 2 (Vagas ESG)
3. 🆕 Criar migrations SQL

### **Curto prazo (2-4 semanas):**
1. Módulo 3 (Profissionais)
2. Módulo 4 (Matching)
3. Importação de 3mil leads

### **Médio prazo (1-3 meses):**
1. Sistema de autenticação
2. Área administrativa
3. Integração pagamentos
4. Deploy em produção

---

## 📞 Contato e Documentação

- **Documentação API:** http://127.0.0.1:8000/docs
- **Copilot Instructions:** `.github/copilot-instructions.md`
- **Roadmap:** `ROADMAP.md`

---

**Última atualização:** 11/10/2025  
**Versão:** 1.0 (Sistema de classificação funcionando)  
**Próxima versão:** 2.0 (Sistema de matching)
