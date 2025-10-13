# 🤖 POC - Scraper de Vagas ESG

## 📋 Objetivo

Proof of Concept para **web scraping automático** de vagas ESG/Sustentabilidade em plataformas de emprego brasileiras.

## 🎯 Escopo do POC

### Sites-alvo (Fase 1):
1. ✅ **Vagas.com** - API pública disponível
2. ⏳ **LinkedIn Jobs** - Requer autenticação
3. ⏳ **Catho** - HTML parsing
4. ⏳ **Indeed** - API disponível

### Palavras-chave ESG:
- Sustentabilidade
- ESG
- Meio Ambiente
- ODS
- Energia Renovável
- Reciclagem
- Carbon Neutral
- Green
- Ambiental

## 🏗️ Estrutura

```
scrapers_poc/
├── README.md              # Este arquivo
├── requirements.txt       # Dependências Python
├── config.py             # Configurações e keywords
├── base_scraper.py       # Classe base abstrata
├── vagas_com_scraper.py  # Scraper Vagas.com
├── test_scraper.py       # Script de teste
└── results/              # Resultados salvos (JSON)
    └── .gitkeep
```

## 🚀 Como Usar

### 1. Instalar dependências

```bash
cd scrapers_poc
pip install -r requirements.txt
```

### 2. Executar teste

```bash
python test_scraper.py
```

### 3. Ver resultados

Os resultados são salvos em `results/vagas_YYYY-MM-DD_HH-MM-SS.json`

## 📊 Estrutura de Dados

Cada vaga extraída contém:

```json
{
  "titulo": "Analista de Sustentabilidade",
  "empresa": "Empresa Verde Ltda",
  "localizacao": "São Paulo - SP",
  "tipo": "CLT",
  "remoto": true,
  "descricao": "Descrição completa da vaga...",
  "requisitos": "Requisitos extraídos...",
  "salario": "R$ 6.000 - R$ 9.000",
  "link_candidatura": "https://vagas.com/exemplo",
  "fonte": "vagas.com",
  "data_scraping": "2025-10-11T21:05:00",
  "keywords_encontradas": ["sustentabilidade", "ESG", "ODS 13"]
}
```

## ✅ Critérios de Sucesso do POC

- [ ] Consegue extrair **mínimo 10 vagas** de Vagas.com
- [ ] Taxa de sucesso > 80% (vagas válidas)
- [ ] Tempo de execução < 2 minutos
- [ ] Identifica corretamente palavras-chave ESG
- [ ] Formato de dados compatível com `vagas_esg` table

## 🔄 Próximos Passos (Pós-POC)

Se aprovado:

1. **Integração com projeto principal**
   - Mover para `Empresas Verdes/scrapers/`
   - Integrar com banco `gjb_dev.db`
   - Adicionar colunas: `origem`, `link_externo`, `scraped_at`

2. **Classificação automática ODS**
   - Usar OpenAI GPT-4 para classificar vagas
   - Extrair habilidades ESG do texto
   - Score de autenticidade (anti-greenwashing)

3. **Automação**
   - APScheduler para rodar a cada 6 horas
   - Dashboard de monitoramento
   - Email com resumo diário

4. **Escalabilidade**
   - Adicionar mais sites (LinkedIn, Catho, Indeed)
   - Proxy rotation (evitar bloqueio)
   - Rate limiting

## ⚠️ Limitações Conhecidas

- **Anti-scraping**: Sites podem bloquear após muitas requisições
- **HTML dinâmico**: Alguns sites requerem JavaScript (Playwright)
- **Manutenção**: HTML muda, scraper quebra (precisa monitoramento)
- **Legal**: Verificar ToS de cada site

## 📝 Decisão

**Bruno deve avaliar:**
- ✅ Qualidade das vagas extraídas
- ✅ Quantidade suficiente para MVP
- ✅ Complexidade de manutenção
- ✅ Risco de bloqueio

**Depois decidir:**
- 🟢 Integrar no projeto principal
- 🟡 Melhorar POC antes
- 🔴 Descartar e buscar alternativa (APIs pagas)

---

**Data:** 2025-10-11  
**Status:** 🚧 Em desenvolvimento  
**Responsável:** GitHub Copilot + Bruno
