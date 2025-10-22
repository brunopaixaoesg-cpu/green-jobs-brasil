# 🗺️ MAPA COMPLETO DE ROTAS - GREEN JOBS BRASIL

## 🌐 ESTRUTURA DE NAVEGAÇÃO

```
http://127.0.0.1:8002/
│
├── 🏠 / (Landing Page)
│   │
│   ├─> Botão "Acessar Dashboard" ──> /dashboard
│   ├─> Link "Ver Empresas" ──> /empresas
│   └─> Link "Sistema ML" ──> /ml-avancado
│
├── 📊 /dashboard (Dashboard Moderno)
│   │
│   ├─> Busca CNPJ ──> /api/search-company/{cnpj}
│   ├─> Estatísticas ──> /api/stats
│   ├─> Lista empresas ──> /api/empresas
│   └─> CNAEs ──> /api/cnaes
│
├── 🏢 /empresas (Empresas Verdes)
│   │
│   ├─> API dados ──> /api/empresas
│   ├─> Filtro por score
│   ├─> Filtro por UF
│   └─> Busca por texto
│
├── 🤖 /ml-avancado (Dashboard ML)
│   │
│   ├─> Stats matching ──> /api/matching/stats
│   ├─> Vagas ──> /api/vagas
│   └─> Profissionais ──> /api/profissionais
│
├── 💼 /vagas (Sistema de Vagas)
│   │
│   └─> API vagas ──> /api/vagas
│
└── ℹ️ /explicacao-matching (Como Funciona)
    │
    └─> Documentação do sistema ML
```

---

## 🔌 ENDPOINTS API (JSON)

### Dados do Sistema
```
GET /api/stats
├─> empresas_verdes: 12
├─> score_medio: 74.6
├─> vagas_disponiveis: 81
└─> profissionais_cadastrados: 120
```

### Empresas
```
GET /api/empresas
└─> [12 empresas com green_score]
```

### Busca CNPJ
```
GET /api/search-company/{cnpj}
├─> Valida 14 dígitos
├─> Consulta ReceitaWS
├─> Calcula green_score
└─> Retorna dados completos
```

### CNAEs Verdes
```
GET /api/cnaes
└─> [6 CNAEs classificados]
```

### Matching ML
```
GET /api/matching/stats
├─> total_candidaturas: 768
├─> score_medio: 68.0
├─> matches_excelentes: 22
└─> precisao_ml: 98.5
```

### Vagas e Profissionais
```
GET /api/vagas
└─> [10 vagas ESG mais recentes]

GET /api/profissionais  
└─> [10 profissionais ativos]
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
C:\Users\Bruno\Empresas Verdes\
│
├── 🚀 START API
│   ├── start_api.py ⭐ (USAR ESTE)
│   └── start_debug.bat
│
├── 🗄️ BANCO DE DADOS
│   └── gjb_dev.db ⭐ (SQLite)
│
├── 🔌 APIs
│   ├── api/sqlite_api_clean.py ⭐ (PRINCIPAL)
│   ├── api_empresas.py
│   └── api_simples.py
│
├── 📄 TEMPLATES
│   └── api/templates/
│       ├── landing_page.html ⭐
│       ├── dashboard_moderno.html ⭐
│       ├── empresas_modernas.html ⭐
│       ├── matching/
│       │   ├── dashboard_ml.html ⭐
│       │   └── explicacao_matching.html ⭐
│       └── vagas/
│           └── lista.html ⭐
│
├── 🧪 TESTES
│   ├── auditoria_completa.py ⭐
│   ├── test_api_completo.py
│   ├── test_dashboard.py
│   └── test_cnpj.py
│
└── 📚 DOCUMENTAÇÃO
    ├── DOCUMENTACAO_COMPLETA.md ⭐
    ├── MAPA_ROTAS.md (este arquivo)
    └── STATUS_FINAL_PROJETO.md
```

---

## 🎯 FLUXO DE USO TÍPICO

### 1️⃣ Usuário Acessa Landing Page
```
http://127.0.0.1:8002/
↓
Vê estatísticas gerais
↓
Clica "Acessar Dashboard"
```

### 2️⃣ Explora Dashboard
```
http://127.0.0.1:8002/dashboard
↓
Vê empresas verdes cadastradas
↓
Busca CNPJ de nova empresa
↓
Sistema consulta Receita Federal
↓
Calcula score verde automaticamente
```

### 3️⃣ Filtra Empresas
```
http://127.0.0.1:8002/empresas
↓
Aplica filtros (score, UF, busca)
↓
Vê detalhes de cada empresa
```

### 4️⃣ Explora Sistema ML
```
http://127.0.0.1:8002/ml-avancado
↓
Vê matches profissional-vaga
↓
Verifica estatísticas de compatibilidade
```

---

## 🔍 EXEMPLOS DE USO

### Buscar Empresa por CNPJ
```javascript
// JavaScript (frontend)
const cnpj = "34028316000103";
fetch(`/api/search-company/${cnpj}`)
  .then(r => r.json())
  .then(data => {
    console.log(data.nome);
    console.log(data.green_score);
  });
```

```python
# Python (backend/testes)
import requests
cnpj = "34028316000103"
r = requests.get(f"http://127.0.0.1:8002/api/search-company/{cnpj}")
data = r.json()
print(data['nome'], data['green_score'])
```

### Listar Empresas com Filtro
```javascript
// Carregar empresas
fetch('/api/empresas')
  .then(r => r.json())
  .then(empresas => {
    // Filtrar por score alto
    const scorAlto = empresas.filter(e => e.green_score >= 80);
    console.log(`${scorAlto.length} empresas com score alto`);
  });
```

---

## 🛠️ COMANDOS DE MANUTENÇÃO

### Iniciar Sistema
```powershell
# Método recomendado
py start_api.py

# Método alternativo (nova janela)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Bruno\Empresas Verdes'; py start_api.py"
```

### Verificar Status
```powershell
# API funcionando?
py -c "import requests; print('API:', requests.get('http://127.0.0.1:8002/').status_code)"

# Quantas empresas?
py -c "import requests; print('Empresas:', len(requests.get('http://127.0.0.1:8002/api/empresas').json()))"

# Banco OK?
py -c "import sqlite3; conn = sqlite3.connect('gjb_dev.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM empresas_verdes'); print('DB:', cursor.fetchone()[0])"
```

### Rodar Testes
```powershell
# Auditoria completa
py auditoria_completa.py

# Teste APIs
py test_api_completo.py

# Teste CNPJ
py test_cnpj.py
```

### Limpar Processos
```powershell
# Ver processos Python
tasklist | findstr python

# Matar todos
taskkill /f /im python.exe

# Ver porta 8002
netstat -ano | findstr :8002
```

---

## 📊 DADOS RETORNADOS POR CADA ENDPOINT

### GET /api/empresas
```json
[
  {
    "cnpj": "88776655000178",
    "razao_social": "Biomassa Energia Verde SA",
    "nome_fantasia": "Biomassa Energia",
    "cnae_principal": "3511-5/04",
    "green_score": 90,
    "situacao_cadastral": "ATIVA",
    "municipio": "Juiz de Fora",
    "uf": "MG",
    "ods_tags": [7, 13, 15]
  }
]
```

### GET /api/stats
```json
{
  "empresas_verdes": 12,
  "score_medio": 74.6,
  "vagas_disponiveis": 81,
  "profissionais_cadastrados": 120,
  "timestamp": "2025-10-16T18:30:00.000000"
}
```

### GET /api/search-company/34028316000103
```json
{
  "nome": "EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS",
  "cnpj": "34.028.316/0001-03",
  "situacao": "ATIVA",
  "municipio": "BRASILIA",
  "uf": "DF",
  "cnaes": ["53.10-5-01", "47.13-0-02"],
  "green_score": 0,
  "is_green": false,
  "atividade_principal": "atividades do correio nacional"
}
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Antes de Usar
- [ ] API rodando na porta 8002
- [ ] Arquivo gjb_dev.db existe
- [ ] Pasta api/templates existe
- [ ] Python com FastAPI instalado

### Durante o Uso
- [ ] Landing page carrega
- [ ] Dashboard mostra estatísticas
- [ ] Empresas aparecem na lista
- [ ] Busca CNPJ funciona
- [ ] Filtros respondem

### Para Debug
- [ ] Verificar logs no terminal
- [ ] Testar endpoints individualmente
- [ ] Verificar banco de dados
- [ ] Rodar auditoria completa

---

**Última atualização:** 16/10/2025  
**Status:** ✅ Totalmente mapeado e funcional