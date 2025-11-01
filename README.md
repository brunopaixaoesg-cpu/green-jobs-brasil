# Green Jobs Brasil 🌱

## 📌 Navegação Rápida

| Documento | Descrição |
|-----------|-----------|
| [📋 ROADMAP.md](ROADMAP.md) | **Prioridades e próximos marcos** (P0-P3 + Q4/Q1) |
| [🧹 PLANO_LIMPEZA.md](PLANO_LIMPEZA.md) | Análise de arquivos e estrutura proposta |
| [▶️ executar_limpeza.ps1](executar_limpeza.ps1) | Script automatizado de limpeza |
| [📊 RESUMO_RETOMADA.md](RESUMO_RETOMADA.md) | Resumo executivo e próximas ações |
| [🗺️ MAPA_ROTAS.md](MAPA_ROTAS.md) | Mapa completo de rotas da API |
| [📖 Como funciona](http://127.0.0.1:8002/explicacao-matching) | Página explicativa da plataforma |

---



**Plataforma de Matching Inteligente para Empregos Verdes no Brasil**Sistema para identificação e classificação de empresas verdes no Brasil baseado em códigos CNAE e mapeamento para Objetivos de Desenvolvimento Sustentável (ODS).



Sistema completo de conexão entre profissionais ESG e empresas sustentáveis, com Machine Learning para compatibilidade, dashboards interativos e storytelling profissional.## ✅ Status do Sistema



---**✅ SISTEMA 100% FUNCIONAL - TESTADO E APROVADO:**

- ✅ **Banco de Dados**: SQLite configurado com 43 CNAEs verdes + 10 empresas exemplo

## ✅ Status do Sistema - v1.6- ✅ **ETL Pipeline**: Processamento de dados com classificação verde completo

- ✅ **API REST**: FastAPI rodando em http://127.0.0.1:8000 com dados reais

**🎉 SISTEMA MVP COMPLETO - TESTADO E FUNCIONAL:**- ✅ **Documentação**: Swagger UI disponível em http://127.0.0.1:8000/docs

- ✅ **ML v3**: Algoritmo de matching realista (47.4% score médio, 0.1% excelente)- ✅ **Endpoints**: /empresas, /cnaes, /stats todos funcionais com banco real

- ✅ **Dashboard Profissional v1.4**: Gestão completa de candidaturas e perfil- ✅ **Launcher**: Scripts simplificados e ultra-confiáveis

- ✅ **Dashboard Empresa v1.5**: Login, gerenciamento de candidatos, ações em tempo real- ✅ **Problemas Resolvidos**: Inicialização, caminhos, dependências

- ✅ **Storytelling v1.6**: Perfis narrativos além do CV tradicional

- ✅ **Autenticação**: Sistema seguro com SHA256 para profissionais e empresas## 🚀 Como Usar

- ✅ **Banco de Dados**: 857 candidaturas, 101 vagas, 120 profissionais, 3 empresas

- ✅ **API REST**: FastAPI rodando em http://127.0.0.1:8002 com 30+ endpoints### Iniciar o Sistema

```bash

---# MÉTODO RECOMENDADO (Ultra-confiável):

python run_green_jobs.py

## 🚀 Início Rápido

# ALTERNATIVO (Windows):

### 1️⃣ Iniciar o Sistemainiciar_green_jobs.bat

```bash

# Windows (Recomendado):# PARA DESENVOLVEDORES:

INICIAR_SISTEMA.batpython start_api.py

```

# Ou via Python:

python start_api.py### Acessar a API

```- **API Base**: http://127.0.0.1:8000

- **Documentação**: http://127.0.0.1:8000/docs

### 2️⃣ Acessar as Interfaces- **Health Check**: http://127.0.0.1:8000/health



**📊 Dashboards Disponíveis:**## 📊 Dados Disponíveis

- **ML Dashboard**: http://127.0.0.1:8002/ml-avancado

- **Dashboard Profissional**: http://127.0.0.1:8002/dashboard/{profissional_id}### Empresas Verdes (10 registros)

- **Login Empresa**: http://127.0.0.1:8002/empresas/loginEmpresas exemplo com pontuação verde calculada baseada em CNAEs sustentáveis.

- **Perfil Storytelling**: http://127.0.0.1:8002/api/profissionais/perfil/{id}

- **Documentação API**: http://127.0.0.1:8002/docs### CNAEs Verdes (43 classificados)

CNAEs mapeados para sustentabilidade com categorização:

**🔑 Credenciais de Teste:**- **Core**: CNAEs centrais de sustentabilidade (ex: energia solar)

- **Adjacent**: CNAEs adjacentes (ex: consultoria ambiental)

**Empresas:**- **Secondary**: CNAEs de apoio (ex: tecnologia da informação)

- `contato1@solarener.com.br` / `senha123` (Solar Energy)

- `contato2@reciclagem.com.br` / `senha456` (Reciclagem Verde)### Relacionamentos Empresa-CNAE (17 registros)

- `contato3@trataragua.com.br` / `senha789` (Tratamento de Água)Vínculos entre empresas e seus CNAEs principais e secundários.



**Profissionais:**## 🎯 Sistema de Pontuação Verde

- Maria Silva Santos (ID: 1) - Analista Ambiental Sênior

- **+80 pontos**: CNAE principal "Core"

---- **+60 pontos**: CNAE principal "Adjacent" 

- **+10 pontos**: Cada CNAE secundário verde (máximo +20)

## 📊 Dados do Sistema- **-50 pontos**: Penalidade para empresas inativas



### 🎯 Machine Learning v3 (Realista)## 📋 Endpoints da API

- **857 candidaturas** simuladas com distribuição realista

- **Score médio**: 47.4% (anteriormente 62.9% - ajustado)### Empresas

- **Distribuição**:- `GET /empresas` - Listar empresas verdes

  - 🟢 Excelente (>80%): 0.1%- `GET /empresas/{cnpj}` - Detalhes de empresa específica

  - 🔵 Bom (60-80%): 23.1%- `GET /empresas/stats/por-uf` - Estatísticas por estado

  - 🟡 Regular (40-60%): 43.9%

  - 🔴 Baixo (<40%): 32.9%### CNAEs

- `GET /cnaes` - Listar CNAEs verdes

### 💼 Vagas Verdes- `GET /cnaes/{codigo}` - Detalhes de CNAE específico

- **101 vagas** ativas em empresas sustentáveis

- Categorias: Energia Renovável, Gestão de Resíduos, Recursos Hídricos, Consultoria ESG### Sistema

- Mapeamento para ODS (Objetivos de Desenvolvimento Sustentável)- `GET /health` - Status da API

- `GET /stats` - Estatísticas gerais

### 👥 Profissionais ESG

- **120 profissionais** cadastrados## 🗂️ Estrutura do Projeto

- **52 campos** de dados (incluindo 12 campos de storytelling)

- Habilidades, certificações, experiências, conquistas```

Empresas Verdes/

### 🏢 Empresas Sustentáveis├── api/                    # API FastAPI

- **3 empresas ESG** de teste│   ├── app.py             # Aplicação principal

- Setores: Energia Solar, Reciclagem, Tratamento de Água│   ├── models.py          # Modelos SQLAlchemy

- Sistema de gestão de candidaturas integrado│   ├── schemas.py         # Schemas Pydantic

│   └── routers/           # Endpoints organizados

---├── etl/                   # Pipeline de dados

│   ├── main.py           # ETL completo

## 🎨 Funcionalidades Principais│   └── config.py         # Configurações

├── db/                    # Banco de dados

### 1. Dashboard Profissional v1.4│   ├── schema_sqlite.sql  # Schema SQLite

**Visão 360º da jornada ESG do profissional**│   └── seed_cnae.sql     # Dados CNAEs verdes

├── data/                  # Dados processados

- 📈 **Estatísticas**: Total de candidaturas, score médio, vagas disponíveis├── gjb_dev.db            # Banco SQLite

- 📋 **Gestão de Candidaturas**: Filtros por status, ordenação, busca├── start_api.py          # Script para iniciar API

- 🎯 **Compatibilidade Visual**: Barras de progresso coloridas por score└── etl_simple.py         # ETL simplificado

- 📊 **Gráficos Interativos**: Candidaturas por status, evolução temporal, distribuição de scores```

- 🔔 **Alertas**: Notificações de mudanças de status em tempo real

## 🔧 Tecnologias

**Endpoint**: `GET /dashboard/{profissional_id}`

- **Python 3.13**: Linguagem principal

### 2. Dashboard Empresa v1.5- **FastAPI**: Framework web para API REST

**Gestão completa de recrutamento verde**- **SQLAlchemy**: ORM para banco de dados

- **SQLite**: Banco de dados local

- 🔐 **Login Seguro**: Autenticação com SHA256- **DuckDB**: Processamento de dados (ETL)

- 📊 **Visão Geral**: Cards de estatísticas (vagas, candidaturas, pendentes)- **Pydantic**: Validação de dados

- 📑 **Tabs por Vaga**: Organização por vaga com contadores de badges- **Uvicorn**: Servidor ASGI

- 🎯 **Filtros Avançados**: Status, score mínimo, ordenação

- 👤 **Modal de Candidatos**: Detalhes completos com barra de compatibilidade## 💡 Próximos Passos

- ⚡ **Ações Rápidas**: 4 botões (Rejeitar, Em Análise, Entrevista, Aprovar)

1. **Expansão de Dados**: Processar datasets completos da RFB

**Endpoints**:2. **Interface Web**: Desenvolver dashboard para visualização

- `POST /empresas/api/login` - Login3. **API Avançada**: Adicionar filtros geográficos e por ODS

- `GET /empresas/dashboard` - Dashboard HTML4. **Deploy**: Publicar em ambiente de produção

- `GET /empresas/api/candidaturas` - Listar com filtros5. **Integrações**: Conectar com fontes externas de dados

- `PUT /empresas/api/candidatura/{id}/status` - Atualizar status

## 🤝 Como Contribuir

### 3. Storytelling Profissional v1.6

**Mostre quem você é além do CV**1. Clone o repositório

2. Instale dependências: `pip install -r api/requirements.txt`

- 🎨 **Banner Personalizado**: Design verde com foto de perfil3. Execute testes: `python -m pytest`

- 📖 **História Verde**: Narrativa da jornada ESG (476 caracteres)4. Contribua com melhorias

- 🏆 **Conquistas**: Cards com ícones, títulos, descrições e datas

- 💼 **Portfólio de Projetos**: ---

  - 3 projetos completos com resultados mensuráveis

  - Tags de ODS com badges coloridos (50px)**Green Jobs Brasil** - Mapeando o futuro sustentável do Brasil 🇧🇷
  - Resultados com impacto (ex: "40% redução emissões")
- 💡 **Valores Pessoais**: Pills gradiente com valores-chave
- 🎯 **Objetivos de Carreira**: Planos e ambições profissionais
- 🌍 **Idiomas**: Badges de proficiência (Nativo, Fluente, Intermediário)
- 🤝 **Voluntariado**: Timeline com marcadores e conexões
- 📚 **Publicações**: Lista de artigos e ebooks com links

**Campos de Storytelling** (12 novos):
- `historia_verde` (TEXT)
- `motivacao` (TEXT)
- `conquistas_json` (JSON)
- `portfolio_projetos_json` (JSON)
- `valores_pessoais` (TEXT)
- `objetivos_carreira` (TEXT)
- `foto_perfil_url` (TEXT)
- `banner_url` (TEXT)
- `redes_sociais_json` (JSON)
- `idiomas_json` (JSON)
- `voluntariado_json` (JSON)
- `publicacoes_json` (JSON)

**Endpoints**:
- `GET /api/profissionais/perfil/{id}` - Página HTML
- `GET /api/profissionais/api/{id}/storytelling` - Dados JSON

### 4. Sistema de Autenticação
**Segurança para profissionais e empresas**

- 🔐 **SHA256**: Hashing seguro de senhas
- 🎫 **Tokens**: Sistema de tokens para sessões
- 👤 **Perfis Separados**: Rotas distintas para profissionais e empresas
- ✅ **Validação**: Verificação de credenciais e permissões

**Endpoints**:
- `POST /auth/register` - Cadastro de profissional
- `POST /auth/login` - Login de profissional
- `POST /empresas/api/login` - Login de empresa

---

## 📋 API Completa - 30+ Endpoints

### 🔐 Autenticação (`/auth`)
- `POST /auth/register` - Registrar profissional
- `POST /auth/login` - Login profissional
- `GET /auth/me` - Perfil do usuário logado

### 👥 Profissionais (`/api/profissionais`)
- `GET /api/profissionais` - Listar profissionais
- `GET /api/profissionais/{id}` - Detalhes do profissional
- `POST /api/profissionais` - Criar profissional
- `PUT /api/profissionais/{id}` - Atualizar profissional
- `GET /api/profissionais/{id}/candidaturas` - Candidaturas do profissional
- `GET /api/profissionais/{id}/estatisticas` - Estatísticas do profissional
- `GET /api/profissionais/perfil/{id}` - Página de storytelling
- `GET /api/profissionais/api/{id}/storytelling` - Dados de storytelling

### 💼 Vagas (`/api/vagas`)
- `GET /api/vagas` - Listar vagas
- `GET /api/vagas/{id}` - Detalhes da vaga
- `POST /api/vagas` - Criar vaga
- `PUT /api/vagas/{id}` - Atualizar vaga
- `GET /api/vagas/{id}/candidatos` - Candidatos da vaga

### 📝 Candidaturas (`/api/candidaturas`)
- `GET /api/candidaturas` - Listar candidaturas
- `GET /api/candidaturas/{id}` - Detalhes da candidatura
- `POST /api/candidaturas` - Criar candidatura
- `PUT /api/candidaturas/{id}` - Atualizar status
- `DELETE /api/candidaturas/{id}` - Cancelar candidatura

### 🏢 Empresas (`/empresas`)
- `POST /empresas/api/login` - Login empresa
- `GET /empresas/dashboard` - Dashboard empresa
- `GET /empresas/api/candidaturas` - Candidaturas com filtros
- `PUT /empresas/api/candidatura/{id}/status` - Atualizar status
- `GET /empresas/api/estatisticas/{id}` - Estatísticas empresa

### 🤖 Machine Learning (`/api/matching`)
- `POST /api/matching/calcular` - Calcular compatibilidade
- `GET /api/matching/recomendacoes/{id}` - Recomendar vagas
- `GET /api/matching/dashboard` - Dashboard ML

---

## 🗂️ Estrutura do Projeto

```
Empresas Verdes/
├── api/                              # API FastAPI
│   ├── sqlite_api_clean.py          # Aplicação principal (entry point)
│   ├── db.py                         # Configuração do banco
│   ├── requirements.txt              # Dependências Python
│   ├── routers/                      # Endpoints organizados
│   │   ├── auth.py                   # Autenticação (registro, login)
│   │   ├── profissionais.py          # 1100+ linhas - CRUD + storytelling
│   │   └── empresas.py               # 350 linhas - Login + dashboard
│   ├── services/                     # Lógica de negócio
│   │   └── ml_service.py            # Algoritmo de matching ML v3
│   ├── templates/                    # HTML Templates
│   │   ├── login.html               # Login profissional
│   │   ├── login_empresa.html       # Login empresa (roxo)
│   │   ├── dashboard_profissional.html  # Dashboard completo
│   │   ├── dashboard_empresa.html   # Dashboard empresa (520 linhas)
│   │   ├── perfil_storytelling.html # Perfil narrativo (750+ linhas)
│   │   └── ml_dashboard.html        # Dashboard ML com gráficos
│   └── static/                       # CSS, JS, imagens
│
├── scripts/                          # Scripts utilitários
│   ├── simulador_dados.py           # Gera 857 candidaturas realistas
│   ├── preparar_demo.py             # Prepara dados para demo
│   ├── criar_tabela_empresas_esg.py # Cria tabela de empresas
│   └── add_storytelling_fields.py   # Adiciona campos storytelling
│
├── ml/                               # Machine Learning
│   └── model_v3.py                  # Algoritmo de matching v3
│
├── tests/                            # Testes automatizados
│   ├── teste_auth.py
│   ├── teste_dashboard_profissional.py
│   ├── teste_dashboard_empresa.py
│   └── teste_fluxo_completo.py
│
├── gjb_dev.db                       # Banco SQLite principal
├── start_api.py                     # Script para iniciar API
├── INICIAR_SISTEMA.bat              # Launcher Windows
└── README.md                        # Este arquivo
```

---

## 🔧 Tecnologias

### Backend
- **Python 3.13**: Linguagem principal
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados local (gjb_dev.db)
- **Pydantic**: Validação de dados e schemas
- **Uvicorn**: Servidor ASGI de alta performance

### Machine Learning
- **Scikit-learn**: Algoritmos de matching
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js**: Gráficos interativos
- **JavaScript ES6**: Interatividade e AJAX
- **Jinja2**: Template engine

### Simulação de Dados
- **Faker**: Geração de dados fictícios
- **Random**: Distribuições estatísticas

---

## 🎯 Algoritmo de Matching ML v3

### Cálculo de Compatibilidade

**Fórmula Base:**
```python
score = (
    match_habilidades * 0.35 +      # 35% - Habilidades ESG
    match_experiencia * 0.25 +       # 25% - Anos de experiência
    match_certificacoes * 0.20 +     # 20% - Certificações
    match_localizacao * 0.10 +       # 10% - Localização (UF)
    match_ods * 0.10                 # 10% - Objetivos ODS
)
```

### Ranges Realistas por Status
- **Aprovada**: 60-80% (média: 70%)
- **Entrevista**: 45-70% (média: 57.5%)
- **Em Análise**: 35-60% (média: 47.5%)
- **Pendente**: 25-50% (média: 37.5%)
- **Rejeitada**: 10-35% (média: 22.5%)

### Resultado
- **Score médio geral**: 47.4%
- **Distribuição realista**: Apenas 0.1% de candidaturas excelentes
- **Defensibilidade**: Scores honestos e explicáveis

---

## 💡 Roadmap - Próximas Funcionalidades

### ⏳ Em Desenvolvimento
- [ ] Edição de perfil storytelling (interface drag-and-drop)
- [ ] Upload de fotos (perfil e banner)
- [ ] Mais profissionais com histórias completas (3-5 perfis)
- [ ] Animações e transições no storytelling

### 🔮 Backlog
- [ ] **Cadastro de Empresas**: Formulário de registro
- [ ] **Criação de Vagas**: Interface para empresas postarem vagas
- [ ] **Notificações por Email**: Sistema de alertas automáticos
- [ ] **Chat Empresa-Candidato**: Comunicação direta na plataforma
- [ ] **Mobile First**: Melhorias de responsividade
- [ ] **Analytics & Admin**: Dashboard de métricas do sistema
- [ ] **Dados Reais**: Scraping e validação de mercado
- [ ] **Deploy**: Publicação em produção (AWS/Heroku)

---

## 🧪 Como Testar

### 1. Testar Dashboard Profissional
```bash
# Iniciar sistema
INICIAR_SISTEMA.bat

# Acessar no navegador
http://127.0.0.1:8002/dashboard/1
```

### 2. Testar Dashboard Empresa
```bash
# Acessar login
http://127.0.0.1:8002/empresas/login

# Credenciais
Email: contato1@solarener.com.br
Senha: senha123

# Testar ações:
- Ver candidaturas por vaga
- Filtrar por status/score
- Aprovar/rejeitar candidatos
- Abrir modal de detalhes
```

### 3. Testar Storytelling
```bash
# Ver perfil de Maria
http://127.0.0.1:8002/api/profissionais/perfil/1

# Verificar:
- Banner e foto carregam
- História Verde aparece
- 3 projetos com ODS badges
- 4 conquistas com ícones
- Valores, idiomas, voluntariado
```

### 4. Rodar Testes Automatizados
```bash
# Teste completo
python teste_fluxo_completo.py

# Teste específico
python teste_dashboard_profissional.py
python teste_dashboard_empresa.py
python teste_auth.py
```

---

## 📖 Documentação Adicional

- **[DOCUMENTACAO_COMPLETA_v1.4.md](DOCUMENTACAO_COMPLETA_v1.4.md)** - Documentação técnica completa
- **[DASHBOARD_EMPRESA_v1.5.md](DASHBOARD_EMPRESA_v1.5.md)** - Guia do Dashboard Empresa
- **[DASHBOARD_PROFISSIONAL_v1.4.md](DASHBOARD_PROFISSIONAL_v1.4.md)** - Guia do Dashboard Profissional
- **[AUTENTICACAO_v1.3.md](AUTENTICACAO_v1.3.md)** - Sistema de autenticação
- **[MAPA_ROTAS.md](MAPA_ROTAS.md)** - Mapa completo de rotas da API
- **[COMO_USAR.md](COMO_USAR.md)** - Guia rápido para usuários

---

## 🤝 Como Contribuir

1. **Fork** o repositório
2. **Clone** para sua máquina local
3. **Instale** dependências: `pip install -r api/requirements.txt`
4. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
5. **Commit** suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
6. **Push** para a branch: `git push origin feature/nova-funcionalidade`
7. **Abra** um Pull Request

---

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Green Jobs Brasil** - Conectando Talentos Verdes com Oportunidades Sustentáveis

🌐 **Website**: [Em desenvolvimento]  
📧 **Email**: contato@greenjobsbrasil.com.br  
🐦 **Twitter**: @GreenJobsBR  
💼 **LinkedIn**: /company/green-jobs-brasil

---

<div align="center">

**🌱 Green Jobs Brasil v1.6**

*Mapeando o futuro sustentável do Brasil* 🇧🇷

**[⭐ Star este projeto](#)** | **[🐛 Reportar Bug](#)** | **[💡 Sugerir Feature](#)**

</div>
