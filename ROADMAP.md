# Roadmap — Green Jobs Brasil (atualizado em 2025-11-01)

> Plataforma para identificar e classificar empresas verdes no Brasil via CNAE e ODS, com API REST, dashboards e matching ML entre profissionais e vagas ESG.

## Visão e objetivos

- Mapear e classificar empresas verdes (Core/Adjacent/Secondary) conectadas a ODS
- Expor dados via API REST e dashboards para profissionais e empresas
- Oferecer matching inteligente (ML) explicável e realista
- Preparar base para escalabilidade (dados RFB) e deploy em produção

## Entregas concluídas (MVP v1.6)

- Banco de dados
  - SQLite com 43 CNAEs verdes e 10 empresas exemplo
  - Relacionamentos empresa ⇄ CNAE; tags ODS e score verde calculado
  - Dados de demonstração: 857 candidaturas, 101 vagas, 120 profissionais
- ETL (etl/main.py)
  - Pipeline DuckDB (+SQLite) com mapeamento CNAE verde e cálculo de score
  - Saída particionada em Parquet por UF; carga no SQLite (empresas_verdes/empresa_cnae)
- API (FastAPI)
  - Endpoints principais: /empresas, /cnaes, /stats, /health, /info (+ documentação Swagger)
  - Rotas adicionais mapeadas em MAPA_ROTAS.md (inclui busca por CNPJ e stats ML)
- Dashboards e UI
  - Dashboard Profissional v1.4 e Dashboard Empresa v1.5 (gestão de vagas/candidaturas)
  - ML Dashboard com estatísticas e visualizações
  - Templates Jinja2 e assets estáticos prontos para demo
- Storytelling Profissional v1.6
  - 12 campos narrativos (história, conquistas, projetos, idiomas, etc.) e página HTML dedicada
- Autenticação v1.3
  - Hash SHA256, sessões por token, login de empresa e rotas separadas
- Operação e DX
  - Scripts de inicialização (start_api.py, INICIAR_SISTEMA.bat) e preparação de demo
  - Testes e utilitários: teste_auth, teste_dashboard_profissional, teste_dashboard_empresa, teste_fluxo_completo, test_api_completo, auditoria_completa
  - Documentação: README, MAPA_ROTAS.md, DOCUMENTACAO_COMPLETA_v1.4.md, guias de uso/deploy

## 🔥 Prioridades imediatas (Nov/2025)

### P0 - Organização e Estabilização
- [x] Criar ROADMAP.md atualizado
- [x] Atualizar página "Como Funciona" com visão completa da plataforma
- [x] **Executar limpeza de projeto**
  - ✅ Removidos 3 backups compactados (~15MB)
  - ✅ Removida pasta backup/ com 107 arquivos (~30MB)
  - ✅ Organizados 40+ scripts em subpastas (scripts/debug, scripts/populacao, etc.)
  - ✅ Movidos 10+ testes para pasta tests/
  - ✅ Arquivada documentação histórica em docs/archived/
  - ✅ Limpo cache Python (__pycache__ e .pyc)
- [x] **Padronizar porta 8002**
  - ✅ Porta padrão: 8002 (definida em start_api.py)
  - ✅ Documentação atualizada
  - ⚠️ Nota: api/main.py é o entrypoint unificado (reexporta sqlite_api_clean.py)

### P1 - Storytelling UX (1 semana)
- [ ] Interface de edição de perfil storytelling
  - Formulário responsivo com validação
  - Upload de foto de perfil e banner (local ou Cloudinary)
  - Preview em tempo real
- [ ] Melhorias Mobile First
  - Ajustar dashboards para mobile (profissional e empresa)
  - Testar em dispositivos reais
  - Otimizar carregamento de imagens

### P2 - API Avançada e KPIs (1 semana)
- [ ] Endpoint `/api/kpis` consolidado
  - Métricas agregadas por período (dia/semana/mês)
  - Tendências de crescimento
  - Top empresas/profissionais/vagas
- [ ] Filtros compostos e paginação
  - Query params padrão: `?page=1&limit=20&sort=score_verde&order=desc`
  - Filtros por ODS, UF, porte, situação cadastral
  - Response headers com `X-Total-Count`, `X-Page`, `X-Per-Page`
- [ ] Cache inteligente
  - Redis ou cache em memória para endpoints de stats
  - TTL configurável por endpoint
  - Invalidação automática em updates

### P3 - Preparação para Deploy (1 semana)
- [ ] Variáveis de ambiente
  - Criar `.env.example` com todas as variáveis
  - Migrar credenciais hardcoded para env vars
  - Validação de env vars obrigatórias no startup
- [ ] CORS e segurança
  - Configurar domínios permitidos via env
  - Rate limiting básico (10 req/s por IP)
  - Headers de segurança (HSTS, CSP básico)
- [ ] Logging estruturado
  - JSON logs para produção
  - Níveis configuráveis (DEBUG/INFO/WARNING/ERROR)
  - Rotation automático de logs
- [ ] Health checks robustos
  - `/health` com check de DB, cache, APIs externas
  - `/ready` para readiness probe (K8s-ready)
  - Métricas Prometheus em `/metrics` (opcional)

## Próximos marcos (Q4/2025 – Q1/2026)

### 1. DATA-01 — Expansão de dados RFB (2 semanas, Dez/2025)
**Objetivo:** Processar datasets completos da Receita Federal e aumentar cobertura nacional.

**Entregas:**
- [ ] Ingestão incremental com DuckDB (processar por lotes de 1M registros)
- [ ] Normalização e deduplicação de CNPJs
- [ ] Validação de dados (situação cadastral, CNAEs válidos)
- [ ] Monitoramento de qualidade (missing data, outliers)
- [ ] Atualização periódica (mensal) do mapeamento CNAE verde
- [ ] Pipeline de scoring em batch para empresas novas

**Métricas de sucesso:**
- 500k+ empresas verdes mapeadas (vs 10 atuais)
- Cobertura de 26 UFs + DF
- Tempo de processamento ETL < 30 min
- Taxa de erro < 0.1%

---

### 2. WEB-01 — Interface Web unificada (2 semanas, Dez/2025)
**Objetivo:** Criar experiência coesa entre landing, empresas, profissionais e ML.

**Entregas:**
- [ ] Design system (cores, tipografia, componentes reutilizáveis)
- [ ] Navegação global consistente (header/footer em todas as páginas)
- [ ] Landing page institucional aprimorada
  - Seções: Hero, Estatísticas, Como Funciona, Depoimentos, CTA
  - Animações sutis (AOS, Intersection Observer)
- [ ] Página de empresas com filtros visuais
  - Mapas interativos (Leaflet ou Google Maps)
  - Cards responsivos com score verde
- [ ] Página de profissionais com busca
  - Filtros por habilidades, ODS, localização
  - Integração com storytelling
- [ ] Dashboard ML acessível e explicável
  - Gráficos interativos (Chart.js ou D3.js)
  - Explicação de cada score

**Métricas de sucesso:**
- Lighthouse score > 90 (Performance, Accessibility, Best Practices)
- Core Web Vitals verdes (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Taxa de rejeição < 40%
- Tempo médio na página > 2 min

---

### 3. API-02 — API avançada com autorização (2 semanas, Jan/2026)
**Objetivo:** Adicionar RBAC, paginação robusta e quotas por plano.

**Entregas:**
- [ ] RBAC (Role-Based Access Control)
  - Perfis: Admin, Empresa, Profissional, Anônimo
  - Permissões granulares por endpoint
  - Middleware de autenticação JWT
- [ ] Paginação cursor-based
  - Evitar offset/limit para grandes datasets
  - Response com `next_cursor`, `prev_cursor`
- [ ] Rate limiting por plano
  - Free: 100 req/h
  - Basic: 1k req/h
  - Pro: 10k req/h
- [ ] API versioning
  - `/api/v1/` para endpoints estáveis
  - `/api/v2/` para novas features
- [ ] OpenAPI 3.0 completo
  - Schemas detalhados
  - Exemplos de request/response
  - Exportar para Postman/Insomnia

**Métricas de sucesso:**
- Zero vazamento de dados (teste de penetração)
- p99 latency < 500ms
- Uptime > 99.9%
- Documentação API com nota > 4.5/5

---

### 4. ML-04 — Matching v4 com explicabilidade (2 semanas, Jan/2026)
**Objetivo:** Melhorar precisão e confiança no sistema de matching.

**Entregas:**
- [ ] Novas features
  - Senioridade inferida (júnior/pleno/sênior/especialista)
  - Taxonomia de habilidades ESG (60+ habilidades mapeadas)
  - Análise de trajetória de carreira (crescimento, mudanças de setor)
  - Match cultural (valores, missão, fit)
- [ ] Explicabilidade (SHAP ou LIME)
  - Mostrar contribuição de cada feature para o score
  - Gráficos de força (force plots)
  - Sugestões de melhoria para candidatos
- [ ] Calibração de scores
  - Garantir que score de 80% signifique 80% de chance real de sucesso
  - Validação com dados históricos de contratações
- [ ] A/B testing framework
  - Comparar v3 vs v4 em produção
  - Métricas: precision@k, recall@k, NDCG

**Métricas de sucesso:**
- Precision@10 > 75% (dos 10 top matches, 7+ são relevantes)
- Recall@50 > 90% (dos candidatos relevantes, 90% estão no top 50)
- Score calibration error < 5%
- Satisfação do usuário com explicações > 4/5

---

### 5. DEP-01 — Deploy de produção (1 semana, Fev/2026)
**Objetivo:** Publicar plataforma em ambiente cloud escalável.

**Entregas:**
- [ ] Escolher provedor (Render, AWS, Railway, Fly.io)
- [ ] Migrar de SQLite para PostgreSQL
  - Schema migration automático (Alembic)
  - Backup diário automático
- [ ] CI/CD pipeline (GitHub Actions)
  - Testes automatizados em PR
  - Deploy automático em merge para main
  - Rollback em caso de falha
- [ ] Observabilidade
  - Logs centralizados (Papertrail, Logtail)
  - Métricas (Prometheus + Grafana ou Datadog)
  - Alertas (PagerDuty, Slack)
- [ ] Plano de recuperação
  - RTO < 4h (Recovery Time Objective)
  - RPO < 1h (Recovery Point Objective)
  - Runbook de incidentes

**Métricas de sucesso:**
- Deploy em < 10 min
- Zero downtime em deploys
- Mean Time to Recovery (MTTR) < 30 min
- Satisfação da equipe DevOps > 4/5

---

### 6. INT-01 — Integrações externas (2 semanas, Fev/2026)
**Objetivo:** Conectar com fontes de dados públicas e privadas.

**Entregas:**
- [ ] ReceitaWS e servidores espelho
  - Fallback automático entre servidores
  - Retry exponencial com jitter
  - Cache distribuído (Redis)
- [ ] Dados públicos estaduais/municipais
  - Secretarias de Meio Ambiente (APIs REST ou scraping)
  - Portais de transparência (licitações verdes)
  - IBGE (dados demográficos e econômicos)
- [ ] APIs de certificação
  - ISO 14001, LEED, AQUA (se disponíveis)
  - Verificação automática de certificados
- [ ] Enriquecimento de dados
  - LinkedIn (via API oficial ou scraping ético)
  - Glassdoor (reviews de empresas)
  - Google Maps (localização precisa)

**Métricas de sucesso:**
- 95% de CNPJs enriquecidos com dados externos
- Taxa de falha de integração < 1%
- Tempo médio de enriquecimento < 5s
- Custo por consulta < R$ 0.01

---

### 7. ADM-01 — Analytics & Admin (1 semana, Fev/2026)
**Objetivo:** Painel administrativo para gestão da plataforma.

**Entregas:**
- [ ] Dashboard de métricas do sistema
  - Usuários ativos (DAU, MAU)
  - Vagas publicadas, candidaturas enviadas
  - Taxa de conversão (match → contratação)
  - Revenue (se aplicável)
- [ ] Gestão de usuários
  - CRUD de empresas e profissionais
  - Aprovação manual de empresas verdes (moderação)
  - Banimento/suspensão de contas
- [ ] Auditoria de ações
  - Log de todas as ações admin
  - Histórico de mudanças em registros críticos
- [ ] Relatórios exportáveis
  - CSV, Excel, PDF
  - Agendamento de relatórios (diário, semanal, mensal)

**Métricas de sucesso:**
- Tempo médio de moderação < 15 min
- Zero ações admin não auditadas
- Satisfação da equipe admin > 4.5/5

## Backlog (consolidado)

- Cadastro de empresas; criação de vagas
- Notificações por email; chat empresa–candidato
- Mobile First amplo; acessibilidade WCAG AA
- Analytics/admin; dados reais (scraping/validação de mercado)

## Métricas de sucesso (indicativas)

- API: uptime ≥ 99%, p95 < 300 ms, erro < 1%
- ETL: tempo total < 15 min/dia, falhas recuperáveis
- Dados: #empresas verdes mapeadas, cobertura por UF
- ML: precisão/calibração do score; explicabilidade (feature importance)
- Qualidade: cobertura de testes, saúde dos endpoints críticos

## Riscos e mitigação

- Qualidade/atualidade RFB e limites de APIs externas → cache, retries, monitoramento
- LGPD e privacidade de dados → minimização, anonimização e controles de acesso
- Performance/concorrência no SQLite → migração gradual para Postgres quando necessário
- Divergência de entrypoints da API → unificar app principal e documentar (ver dívida técnica)

## Linha do tempo sugerida

- Nov/2025: Storytelling UX, filtros avançados e preparação de deploy
- Dez/2025: Deploy beta, observabilidade e ingestão RFB inicial
- Jan–Fev/2026: ML v4, RBAC e interface unificada

## Dívida técnica rastreável

- Unificar entrypoint da API (api/main.py vs api/sqlite_api_clean.py e README)
- Padronizar nomes de rotas e portas (8000 vs 8002) e atualizar a documentação
- Limpar e reorganizar README (há conteúdo duplicado/desformatado)

---

Para progresso contínuo e histórico de mudanças, considerar adicionar CHANGELOG.md e etiquetas (epics) nas issues: DATA-01, WEB-01, API-02, ML-04, DEP-01, INT-01, ADM-01.