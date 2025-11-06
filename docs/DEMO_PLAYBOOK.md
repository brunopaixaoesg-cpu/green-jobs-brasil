# Green Jobs Brasil — Playbook de Demonstração Completa (Windows)

Este guia reúne, em um único roteiro, tudo que você precisa para entender o sistema, preparar o ambiente, popular dados demo, iniciar a API e demonstrar as funcionalidades ponta a ponta para clientes e parceiros.

---

## Visão geral do sistema

- Backend: FastAPI (Uvicorn) + SQLite
- Entrada principal: `api/main.py` (reexporta `api/sqlite_api_clean.py`)
- Banco: `api/gjb_dev.db` (inicializado idempotente por `api.db.init_database()`)
- Páginas HTML (Jinja2) servidas por `api/sqlite_api_clean.py`
- Rotas avançadas (filtros/paginação): Routers em `api/routers/` e página visual `GET /test-api`
- Scripts de dados: pasta `scripts/` (popular demo, gerar profissionais e vagas, smoke tests)

Arquivos-chave:
- `start_api.py`: inicia a API em 127.0.0.1:8002
- `api/main.py`: ponto unificado da aplicação
- `api/sqlite_api_clean.py`: app com páginas e endpoints + inclusão dos routers (profissionais, empresas, vagas, kpis)
- `api/templates/test_api_avancada.html`: UI de teste dos filtros/paginação
- `scripts/popular_dados_demo.py`: cria dados realistas (profissionais, empresas, vagas, candidaturas)
- `scripts/full_smoke_test.py`: valida endpoints principais

---

## Funcionalidades que você pode demonstrar

1) Profissionais ESG
- Listagem com filtros compostos (UF, ODS, área, anos de ESG, remoto, nível)
- Paginação e ordenação (nome, experiência, data)
- Storytelling e campos de perfil (quando preenchidos)

2) Empresas Verdes
- Score ESG (0–100) e ODS
- Vagas por empresa e contadores de candidaturas
- Listagem com filtros (UF, ODS, setor, score mínimo), paginação e sorting

3) Vagas Ambientais
- Filtros por UF/ODS/nível/salário mínimo/remoto/híbrido
- Enriquecimento com nome e score da empresa, total de candidaturas
- Paginação + ordenação

4) KPIs e Matching
- KPIs gerais e de matching em `/api/kpis/*` e `/api/matching/*`
- Dashboard de ML (placeholder) em `/ml-avancado`

5) Páginas HTML
- Landing e dashboards de empresa e profissional
- Página interativa de testes de API: `/test-api`

---

## Passo a passo — demo confiável (Windows PowerShell)

Se preferir automatizar tudo, vá direto para: scripts/demo_playbook.ps1

1) Pré-requisitos
- Python 3.13 instalado e no PATH
- Repositório aberto em: `C:\Users\Bruno\Empresas Verdes`

2) Instalar dependências (uma vez)
- Use o arquivo `requirements.txt` na raiz (cobre a API); se faltar algo, use também `api/requirements.txt`.

3) Criar pastas de upload (opcional, para testes de upload)
- `api/static/uploads/profissionais`

4) Iniciar a API
- Método recomendado: `start_api.py` (lança `uvicorn api.main:app` na porta 8002)
- Observação: se a porta 8002 estiver ocupada, finalize o processo Python ou altere a porta.

5) Verificar saúde
- GET `http://127.0.0.1:8002/api/status` (estruturas)
- GET `http://127.0.0.1:8002/docs` (Swagger)

6) Popular banco rapidamente
- GET `http://127.0.0.1:8002/api/populate` (seed simples)
- Alternativa mais rica: `python scripts/popular_dados_demo.py`

7) Rodar smoke test (opcional)
- `python scripts/full_smoke_test.py` (confere endpoints principais e fluxo simples de auth)

8) Abrir as páginas para a demo
- `/test-api` — UI de filtros/paginação (profissionais, empresas, vagas)
- `/empresas/dashboard` — painel de empresa (lista vagas + candidaturas)
- `/vagas` — listagem para candidatos
- `/kpis` — vitrine de KPIs
- `/docs` — documentação interactiva dos endpoints

Links rápidos:
- API base: http://127.0.0.1:8002
- Docs: http://127.0.0.1:8002/docs
- Teste API avançada: http://127.0.0.1:8002/test-api
- Dashboard empresa: http://127.0.0.1:8002/empresas/dashboard
- Vagas (UI): http://127.0.0.1:8002/vagas
- KPIs: http://127.0.0.1:8002/kpis

---

## Roteiro sugerido (10–15 minutos)

1) Abertura (1 min)
- Mostrar `/docs` e `/kpis` para passar visão de produto e maturidade

2) Profissionais (3–4 min)
- Abrir `/test-api` (tab Profissionais)
- Filtrar por UF=SP,RJ; ODS=7,13; Exp mínima=3; Nível=pleno/sênior
- Paginar e ordenar por experiência

3) Empresas (3–4 min)
- Ainda em `/test-api`, tab Empresas
- Aplicar filtros: UF=SP; Score mínimo=70; Setor=Energia
- Mostrar total de vagas e candidaturas por empresa

4) Vagas (3–4 min)
- Tab Vagas
- Filtrar por UF=SP; Salário mínimo=7000; Remoto=Sim; Nível=pleno
- Destacar enriquecimento com informações da empresa e candidaturas

5) Encerramento (1–2 min)
- Abrir `/empresas/dashboard` para visão de uma empresa
- Relembrar que a demonstração é apoiada por dados demo reproduzíveis

---

## Quando “nem tudo inicia” no start_api.py

- O entrypoint ativo é `api/main.py`, que reexporta o app de `api/sqlite_api_clean.py` e, durante o import, tenta incluir routers (profissionais, empresas, vagas, kpis). Se algum router falhar, o app ainda sobe, mas aquela rota específica pode ficar indisponível.
- Causas comuns:
  - Porta 8002 ocupada (outro Python rodando). Solução: encerrar processo na porta 8002.
  - Dependência pendente. Solução: `pip install -r requirements.txt` (e, se necessário, também `pip install -r api/requirements.txt`).
  - Banco sem tabelas esperadas. Solução: o `init_database()` é idempotente; acione `GET /api/populate` ou rode `scripts/popular_dados_demo.py`.
- Dica: o script `restart_and_test_kpis.bat` já automatiza parar/processar/validar KPIs básicos; ele é um bom termômetro.

---

## Endpoints e páginas mais usados na demo

- Profissionais: `GET /api/profissionais?uf=SP,RJ&ods=7,13&anos_exp_min=3&nivel=pleno&sort=anos_experiencia_esg&order=desc&page=1&limit=10`
- Empresas: `GET /empresas/api/listar?uf=SP&score_min=70&setor=energia&sort=score_verde&order=desc&page=1&limit=10`
- Vagas: `GET /api/vagas?uf=SP&salario_min=7000&remoto=true&nivel=pleno&sort=salario_max&order=desc&page=1&limit=10`
- KPIs gerais: `GET /api/kpis/gerais`
- Página UI de teste: `GET /test-api`

Cabeçalhos padrão nas listas:
- `X-Total-Count`, `X-Page`, `X-Total-Pages`, `X-Per-Page`

Formato de resposta padrão nas listas:
```json
{
  "data": [ ... ],
  "pagination": { "total": 123, "page": 1, "pages": 13, "limit": 10, "has_next": true, "has_prev": false },
  "filtros_aplicados": { ... },
  "ordenacao": { "sort": "campo", "order": "asc|desc" }
}
```

---

## Automação em 1 comando

Use o script `scripts/demo_playbook.ps1` para:
- Garantir dependências, pastas e porta livre
- Subir a API (8002) e aguardar ficar online
- Popular dados demo (via endpoint ou script)
- Rodar um smoke test curto
- Abrir as páginas da demo no navegador

Execução:
```powershell
# No PowerShell
cd "C:\Users\Bruno\Empresas Verdes"
powershell -ExecutionPolicy Bypass -File .\scripts\demo_playbook.ps1
```

---

## Troubleshooting rápido

- Porta 8002 ocupada: finalize processos Python (Task Manager) ou execute `netstat -ano | findstr :8002` e `taskkill /f /pid <PID>`
- API sobe mas rota 404/500: veja logs do terminal e verifique `api/sqlite_api_clean.py` (mensagens de carregamento dos routers). Rerode `GET /api/populate`.
- Dependências: reinstale com `pip install -r requirements.txt` (e/ou `api/requirements.txt`).

---

## Apêndice — Scripts úteis

- `scripts/popular_dados_demo.py`: popula profissionais, empresas, vagas, candidaturas (dataset robusto)
- `scripts/gerar_profissionais_ambientais.py`: foca em perfis ambientais realistas
- `scripts/gerar_vagas_ambientais.py`: vagas ambientais por empresas reais
- `scripts/full_smoke_test.py`: checagem rápida de rotas-chave
- `scripts/run_all_tests.py`: roda smoke + suíte `tests/`

---

Pronto. Com este playbook + script, você tem uma demo repetível, com dados ricos e uma UI de filtros que mostra o valor rapidamente.