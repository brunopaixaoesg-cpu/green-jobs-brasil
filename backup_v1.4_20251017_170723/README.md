# Green Jobs Brasil 🌱

Sistema para identificação e classificação de empresas verdes no Brasil baseado em códigos CNAE e mapeamento para Objetivos de Desenvolvimento Sustentável (ODS).

## ✅ Status do Sistema

**✅ SISTEMA 100% FUNCIONAL - TESTADO E APROVADO:**
- ✅ **Banco de Dados**: SQLite configurado com 43 CNAEs verdes + 10 empresas exemplo
- ✅ **ETL Pipeline**: Processamento de dados com classificação verde completo
- ✅ **API REST**: FastAPI rodando em http://127.0.0.1:8000 com dados reais
- ✅ **Documentação**: Swagger UI disponível em http://127.0.0.1:8000/docs
- ✅ **Endpoints**: /empresas, /cnaes, /stats todos funcionais com banco real
- ✅ **Launcher**: Scripts simplificados e ultra-confiáveis
- ✅ **Problemas Resolvidos**: Inicialização, caminhos, dependências

## 🚀 Como Usar

### Iniciar o Sistema
```bash
# MÉTODO RECOMENDADO (Ultra-confiável):
python run_green_jobs.py

# ALTERNATIVO (Windows):
iniciar_green_jobs.bat

# PARA DESENVOLVEDORES:
python start_api.py
```

### Acessar a API
- **API Base**: http://127.0.0.1:8000
- **Documentação**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 📊 Dados Disponíveis

### Empresas Verdes (10 registros)
Empresas exemplo com pontuação verde calculada baseada em CNAEs sustentáveis.

### CNAEs Verdes (43 classificados)
CNAEs mapeados para sustentabilidade com categorização:
- **Core**: CNAEs centrais de sustentabilidade (ex: energia solar)
- **Adjacent**: CNAEs adjacentes (ex: consultoria ambiental)
- **Secondary**: CNAEs de apoio (ex: tecnologia da informação)

### Relacionamentos Empresa-CNAE (17 registros)
Vínculos entre empresas e seus CNAEs principais e secundários.

## 🎯 Sistema de Pontuação Verde

- **+80 pontos**: CNAE principal "Core"
- **+60 pontos**: CNAE principal "Adjacent" 
- **+10 pontos**: Cada CNAE secundário verde (máximo +20)
- **-50 pontos**: Penalidade para empresas inativas

## 📋 Endpoints da API

### Empresas
- `GET /empresas` - Listar empresas verdes
- `GET /empresas/{cnpj}` - Detalhes de empresa específica
- `GET /empresas/stats/por-uf` - Estatísticas por estado

### CNAEs
- `GET /cnaes` - Listar CNAEs verdes
- `GET /cnaes/{codigo}` - Detalhes de CNAE específico

### Sistema
- `GET /health` - Status da API
- `GET /stats` - Estatísticas gerais

## 🗂️ Estrutura do Projeto

```
Empresas Verdes/
├── api/                    # API FastAPI
│   ├── app.py             # Aplicação principal
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Schemas Pydantic
│   └── routers/           # Endpoints organizados
├── etl/                   # Pipeline de dados
│   ├── main.py           # ETL completo
│   └── config.py         # Configurações
├── db/                    # Banco de dados
│   ├── schema_sqlite.sql  # Schema SQLite
│   └── seed_cnae.sql     # Dados CNAEs verdes
├── data/                  # Dados processados
├── gjb_dev.db            # Banco SQLite
├── start_api.py          # Script para iniciar API
└── etl_simple.py         # ETL simplificado
```

## 🔧 Tecnologias

- **Python 3.13**: Linguagem principal
- **FastAPI**: Framework web para API REST
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados local
- **DuckDB**: Processamento de dados (ETL)
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

## 💡 Próximos Passos

1. **Expansão de Dados**: Processar datasets completos da RFB
2. **Interface Web**: Desenvolver dashboard para visualização
3. **API Avançada**: Adicionar filtros geográficos e por ODS
4. **Deploy**: Publicar em ambiente de produção
5. **Integrações**: Conectar com fontes externas de dados

## 🤝 Como Contribuir

1. Clone o repositório
2. Instale dependências: `pip install -r api/requirements.txt`
3. Execute testes: `python -m pytest`
4. Contribua com melhorias

---

**Green Jobs Brasil** - Mapeando o futuro sustentável do Brasil 🇧🇷