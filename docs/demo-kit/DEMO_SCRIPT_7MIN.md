# Roteiro de Demonstração (7–10 min)

Objetivo: mostrar, de forma objetiva, que o GJB já entrega valor com dados de demo e endpoints avançados prontos.

Tempo total sugerido: 7–10 min

---

## 0:00–1:00 — Contexto rápido
- O Green Jobs Brasil conecta profissionais ESG com empresas verdes.
- Backend FastAPI, banco SQLite e endpoints com filtros/paginação/sorting.
- Temos uma UI de teste e um playbook para conduzir a apresentação.

Abrir: /docs e /kpis (2 abas)

---

## 1:00–3:00 — Profissionais ESG
- Ir para /test-api (tab Profissionais)
- Aplicar: UF=SP,RJ, ODS=7,13, Mín. ESG=3, Nível=Pleno
- Ordenar por experiência e paginar

Mensagens-chave:
- Filtros compostos e resposta padronizada (dados, paginação, filtros, ordenação)
- Headers de paginação (X-Total-Count, X-Page, X-Total-Pages, X-Per-Page)

---

## 3:00–5:00 — Empresas Verdes
- Ainda em /test-api (tab Empresas)
- Filtros: UF=SP, Score mínimo=70, Setor=Energia
- Destacar: total de vagas, vagas ativas e candidaturas por empresa

Mensagens-chave:
- Score Verde (0–100) e ODS
- Métricas por empresa (prontas para dashboards)

---

## 5:00–7:00 — Vagas Verdes
- Tab Vagas
- Filtros: UF=SP, Remoto=Sim, Salário mínimo=7000, Nível=Pleno
- Ordenar por salário

Mensagens-chave:
- Enriquecimento com info da empresa e total de candidaturas
- Preparado para matching e funil de recrutamento

---

## 7:00–8:00 — Encerramento executivo
- Abrir /empresas/dashboard
- Reforçar evolução: P1 (estrutura), P2 (filtros, paginação, sorting), próximos passos P3 (deploy)

---

## Anexos úteis
- One-pager de valor: ONEPAGER_CLIENTES.md
- Playbook Visual: /demo-playbook
- Scripts:
  - .\scripts\demo_playbook.ps1
  - .\scripts\demo_capture.ps1
