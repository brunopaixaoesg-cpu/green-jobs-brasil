# Integração Taxonomia Sustentável Brasileira
## Green Jobs Brasil - Plano Estratégico

**Data**: Novembro 2025  
**Status**: Planejamento  
**Prioridade**: ALTA - Vantagem Competitiva Crítica

---

## 🎯 Oportunidade Estratégica

### Por que AGORA é o momento perfeito?

1. **Timing de Mercado**
   - Taxonomia BR em consulta pública (cadernos setoriais lançados)
   - Empresas ainda sem ferramentas de compliance
   - Governo precisará de soluções para implementação
   - Zero concorrentes com integração pronta

2. **Vantagem Competitiva**
   - **First-mover**: Única plataforma CNAE → Taxonomia BR → ODS
   - **Legitimidade**: Alignment com política pública oficial
   - **B2G acelerado**: Contratos governamentais para implementação
   - **Compliance market**: Empresas obrigadas a se classificar

3. **Posicionamento**
   - De "plataforma de empregos verdes" para "infraestrutura nacional de taxonomia sustentável"
   - Narrativa COP30: "Primeira plataforma brasileira aligned com taxonomia oficial"
   - Credibilidade institucional para investidores e governo

---

## 📊 Análise Comparativa: Taxonomias Internacionais

### EU Taxonomy (Referência Global)
- **Estrutura**: 6 objetivos ambientais + critérios técnicos de screening
- **Cobertura**: ~70% das emissões EU (energia, transporte, construção, manufatura)
- **Implementação**: Obrigatória para empresas listadas (NFRD)
- **Critérios**: Thresholds quantitativos (ex: <100gCO2/kWh para energia)

### China Green Bond Catalogue
- **Estrutura**: Lista de atividades elegíveis por setor
- **Foco**: Energia limpa, transporte sustentável, prevenção de poluição
- **Aplicação**: Mercado de títulos verdes

### ASEAN Taxonomy
- **Estrutura**: Traffic light system (verde/âmbar/vermelho)
- **Flexibilidade**: Considera diferentes estágios de desenvolvimento dos países

### **Taxonomia BR - Expectativas**
Baseado em tendências internacionais e contexto brasileiro:
- Alinhamento com ODS (prioridade brasileira)
- Foco em bioeconomia e amazônia (diferencial BR)
- Integração com CNAE (sistema já existente)
- Critérios adaptados à realidade nacional

---

## 🔍 Perguntas Críticas (Para Análise dos Cadernos)

### 1. Estrutura da Taxonomia
- [ ] **Modelo adotado**: Lista positiva (atividades verdes) ou traffic light (verde/transição/não-elegível)?
- [ ] **Base de classificação**: Usa CNAE como referência ou cria nova taxonomia?
- [ ] **Granularidade**: Nível de detalhamento (seção/divisão/grupo/classe/subclasse CNAE)?
- [ ] **Interoperabilidade**: Menciona alinhamento com EU Taxonomy ou outras taxonomias?

### 2. Setores Cobertos
- [ ] Quais setores têm cadernos publicados?
- [ ] Há priorização de setores (Fase 1, 2, 3)?
- [ ] Setores ausentes mas relevantes para empregos verdes?
- [ ] Bioeconomia e Amazônia têm tratamento especial?

### 3. Critérios Técnicos
- [ ] **Tipo**: Quantitativos (thresholds) ou qualitativos (descritivos)?
- [ ] **DNSH (Do No Significant Harm)**: Há critérios de salvaguarda ambiental?
- [ ] **Social safeguards**: Critérios sociais além dos ambientais?
- [ ] **Adaptação climática**: Separado de mitigação?

### 4. Implementação
- [ ] **Timeline**: Quando entra em vigor?
- [ ] **Obrigatoriedade**: Quais empresas serão obrigadas a reportar?
- [ ] **Faseamento**: Implementação gradual ou total?
- [ ] **Penalidades**: Há sanções para não-compliance?

### 5. Governança
- [ ] **Órgão responsável**: Quem administra a taxonomia?
- [ ] **Revisão**: Periodicidade de atualização?
- [ ] **Consulta pública**: Como contribuir?
- [ ] **Dados abertos**: Taxonomia será disponibilizada publicamente?

---

## 🛠️ Plano de Integração Técnica

### Fase 1: Análise e Mapeamento (2-3 semanas)

#### 1.1 Análise Documental
**Objetivo**: Compreender estrutura completa da Taxonomia BR

**Tarefas**:
- [ ] Ler todos os cadernos setoriais publicados
- [ ] Extrair atividades elegíveis por setor
- [ ] Mapear critérios técnicos (quantitativos/qualitativos)
- [ ] Identificar gaps entre CNAE atual e Taxonomia BR
- [ ] Documentar diferenças vs. EU Taxonomy

**Entregáveis**:
- `docs/ANALISE_TAXONOMIA_BR.md` - Análise completa
- `data/taxonomia_br/setores_elegiveis.csv` - Lista de setores
- `data/taxonomia_br/criterios_tecnicos.json` - Critérios estruturados

#### 1.2 Mapeamento CNAE → Taxonomia BR
**Objetivo**: Criar correspondência precisa entre sistemas

**Tarefas**:
- [ ] Mapear CNAEs verdes atuais (43) para categorias da Taxonomia BR
- [ ] Identificar novos CNAEs elegíveis segundo Taxonomia BR
- [ ] Classificar por nível de alinhamento (Core/Adjacent/Secondary)
- [ ] Documentar CNAEs em zona cinzenta (transição)

**Entregáveis**:
- `data/taxonomia_br/mapeamento_cnae_taxonomia.csv`
- Script: `etl/taxonomia_br_mapper.py`

#### 1.3 Análise de Impacto
**Objetivo**: Quantificar impacto na base atual

**Tarefas**:
- [ ] Quantos CNAEs novos serão adicionados?
- [ ] Quantas empresas atuais se enquadram na Taxonomia BR?
- [ ] Quantos empregos verdes adicionais serão identificados?
- [ ] Impacto no score verde das empresas

**Entregáveis**:
- `docs/IMPACTO_TAXONOMIA_BR.md` - Relatório de impacto

---

### Fase 2: Modelagem de Dados (1-2 semanas)

#### 2.1 Schema Extension
**Objetivo**: Adicionar campos para Taxonomia BR

```sql
-- Nova tabela: taxonomia_br_atividades
CREATE TABLE taxonomia_br_atividades (
    id INTEGER PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,  -- Código da atividade na Taxonomia BR
    nome VARCHAR(500) NOT NULL,
    setor VARCHAR(100),  -- Energia, Transporte, Construção, etc.
    categoria VARCHAR(50),  -- Verde, Transição, Não-elegível
    objetivo_ambiental VARCHAR(100),  -- Mitigação, Adaptação, etc.
    criterios_tecnicos JSON,  -- Thresholds e requisitos
    cnae_relacionados JSON,  -- Array de CNAEs mapeados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nova tabela: empresas_taxonomia_br
CREATE TABLE empresas_taxonomia_br (
    id INTEGER PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    atividade_taxonomia_id INTEGER,
    nivel_alinhamento VARCHAR(20),  -- Total, Parcial, Em-transição
    score_conformidade DECIMAL(5,2),  -- 0-100
    criterios_atendidos JSON,
    ultima_avaliacao TIMESTAMP,
    FOREIGN KEY (atividade_taxonomia_id) REFERENCES taxonomia_br_atividades(id)
);

-- Extensão da tabela empresas_esg
ALTER TABLE empresas_esg ADD COLUMN taxonomia_br_status VARCHAR(50);
ALTER TABLE empresas_esg ADD COLUMN taxonomia_br_score DECIMAL(5,2);
ALTER TABLE empresas_esg ADD COLUMN taxonomia_br_categoria VARCHAR(50);
```

#### 2.2 Score Recalibration
**Objetivo**: Atualizar sistema de pontuação verde

**Novo algoritmo**:
```python
def calculate_green_score_v2(empresa):
    """
    Score Verde v2.0 - Integrado com Taxonomia BR
    
    Componentes:
    - 40%: Alinhamento com Taxonomia BR (oficial)
    - 30%: CNAEs verdes (nossa classificação proprietária)
    - 20%: ODS mapping (impacto social-ambiental)
    - 10%: Indicadores adicionais (certificações, iniciativas)
    """
    score = 0
    
    # 1. Taxonomia BR (40 pontos)
    if empresa.taxonomia_br_categoria == 'Verde':
        score += 40
    elif empresa.taxonomia_br_categoria == 'Transição':
        score += 20
    
    # 2. CNAE Verde (30 pontos)
    if empresa.cnae_principal in CNAES_CORE:
        score += 30
    elif empresa.cnae_principal in CNAES_ADJACENT:
        score += 20
    elif empresa.cnae_principal in CNAES_SECONDARY:
        score += 10
    
    # 3. ODS (20 pontos)
    ods_score = calculate_ods_alignment(empresa)
    score += ods_score * 0.2
    
    # 4. Indicadores adicionais (10 pontos)
    bonus = 0
    if empresa.certificacoes:
        bonus += 5
    if empresa.iniciativas_sustentabilidade:
        bonus += 5
    score += min(bonus, 10)
    
    return min(score, 100)
```

---

### Fase 3: Desenvolvimento de Features (3-4 semanas)

#### 3.1 API Endpoints - Taxonomia BR

**Novos endpoints**:

```python
# GET /api/taxonomia-br/atividades
# Lista todas as atividades da Taxonomia BR
# Query params: setor, categoria, objetivo_ambiental

# GET /api/taxonomia-br/atividades/{codigo}
# Detalhes de uma atividade específica

# GET /api/taxonomia-br/mapeamento-cnae/{cnae}
# Retorna atividades da Taxonomia BR para um CNAE

# POST /api/empresas/{cnpj}/avaliar-taxonomia
# Avalia conformidade de uma empresa com Taxonomia BR
# Body: { criterios_declarados: {...} }

# GET /api/empresas/{cnpj}/relatorio-taxonomia
# Gera relatório de conformidade com Taxonomia BR
# Format: JSON, PDF, CSV

# GET /api/stats/taxonomia-br
# Estatísticas gerais da Taxonomia BR na plataforma
# - Total de atividades por categoria
# - Total de empresas por nível de alinhamento
# - Setores mais representados
```

#### 3.2 Dashboard de Conformidade (Empresas)

**Features para o dashboard das empresas**:

1. **Widget de Conformidade Taxonomia BR**
   - Status atual: Verde / Transição / Não-elegível / Não-avaliado
   - Score de conformidade (0-100)
   - Atividades elegíveis identificadas
   - Critérios técnicos atendidos vs. pendentes

2. **Guia de Auto-Avaliação**
   - Checklist interativo de critérios técnicos
   - Upload de evidências (certificados, relatórios)
   - Simulador de score

3. **Relatório Exportável**
   - PDF formatado para apresentar a órgãos reguladores
   - Histórico de avaliações
   - Recomendações de melhoria

#### 3.3 Painel Analítico (Admin/B2G)

**Dashboard para governo e análise macro**:

1. **Visão Geral Nacional**
   - Total de empresas por categoria Taxonomia BR
   - Mapa de calor: estados com maior conformidade
   - Evolução temporal da adoção

2. **Análise Setorial**
   - Comparativo entre setores
   - Identificação de gaps (setores com baixa conformidade)
   - Potencial de empregos verdes por setor

3. **Insights para Política Pública**
   - Setores que precisam de incentivo
   - Regiões com baixa adoção
   - Sugestões de critérios para revisão da taxonomia

---

### Fase 4: Conteúdo e Comunicação (2 semanas)

#### 4.1 Materiais Educacionais

**Criar**:
- [ ] Guia completo: "O que é a Taxonomia Sustentável Brasileira?"
- [ ] FAQ para empresas: "Como se adequar à Taxonomia BR?"
- [ ] Webinar series: "Taxonomia BR na prática"
- [ ] Cases de sucesso: Primeiras empresas conformes

#### 4.2 Atualizações de Marketing

**Narrativa atualizada**:
> "Green Jobs Brasil: A primeira plataforma brasileira integrada com a Taxonomia Sustentável Brasileira oficial. Conectamos empresas conformes com os 7 milhões de empregos verdes que o Brasil vai criar até 2030."

**Materiais para atualizar**:
- [ ] Site institucional
- [ ] Apresentação COP30 (adicionar seção Taxonomia BR)
- [ ] Pitch deck para investidores
- [ ] Material de vendas B2G

#### 4.3 PR e Posicionamento

**Estratégia de comunicação**:
1. **Press release**: "Green Jobs Brasil lança primeira integração com Taxonomia BR"
2. **Artigo técnico**: LinkedIn/Medium sobre a integração
3. **Participação em consulta pública**: Contribuir oficialmente com feedback
4. **Parcerias institucionais**: Aproximação com órgão gestor da Taxonomia

---

## 💰 Modelo de Negócio - Taxonomia BR

### Novos Produtos e Serviços

#### 1. **Taxonomia BR Compliance Suite** (B2B)
**Para empresas que precisam se adequar**

**Tier Básico** (R$ 500/mês):
- Auto-avaliação de conformidade
- Relatório básico de alinhamento
- 1 reavaliação/trimestre

**Tier Profissional** (R$ 2.000/mês):
- Avaliação assistida por especialistas
- Relatórios customizados para reguladores
- Monitoramento contínuo de conformidade
- Alertas de mudanças na taxonomia
- 10 reavaliações/mês

**Tier Enterprise** (R$ 10.000+/mês):
- Multi-unidades de negócio
- Integração API com sistemas ERP
- Consultoria especializada
- Relatórios para investidores (TCFD, ISSB)
- Unlimited avaliações

#### 2. **Taxonomia BR Analytics** (B2G)
**Para governos e órgãos reguladores**

**Contrato anual**: R$ 500.000 - R$ 2.000.000
- Dashboard nacional de conformidade
- Relatórios setoriais e regionais
- Análise de impacto de políticas públicas
- Identificação de setores prioritários
- Suporte técnico para revisão da taxonomia

#### 3. **Green Jobs Verification** (B2B Premium)
**Selo de conformidade com Taxonomia BR**

**Certificação anual**: R$ 5.000 - R$ 50.000 (baseado em porte)
- Auditoria de conformidade
- Selo "Taxonomia BR Verified"
- Destaque na plataforma
- Marketing kit (selos, banners)

---

## 📈 Projeções de Impacto

### Impacto Técnico
- **CNAEs verdes**: De 43 para ~80-120 (estimativa baseada em EU Taxonomy)
- **Empresas elegíveis**: De ~500 para ~5.000+ (expansão 10x)
- **Empregos verdes identificados**: De ~50k para ~500k+
- **Cobertura setorial**: De 10 setores para 20+ setores

### Impacto de Negócio (12 meses pós-lançamento)
- **Receita Compliance Suite**: 200 empresas × R$ 2.000/mês = R$ 400k/mês
- **Contratos B2G**: 3 estados × R$ 500k/ano = R$ 1,5M/ano
- **Certificações**: 100 empresas × R$ 10k/ano = R$ 1M/ano
- **Total ARR**: ~R$ 7M (conservador)

### Impacto Estratégico
- **Legitimidade**: Alinhamento com política pública oficial
- **Barreira de entrada**: 6-12 meses de vantagem sobre concorrentes
- **Network effects**: Empresas certificadas atraem profissionais
- **B2G pipeline**: Abertura para contratos governamentais de longo prazo

---

## 🎯 Quick Wins (Primeiras 2 semanas)

### Ações Imediatas

1. **Análise dos Cadernos** (3 dias)
   - Ler e documentar todos os cadernos publicados
   - Extrair atividades elegíveis
   - Identificar CNAEs de overlap

2. **Comunicação Estratégica** (2 dias)
   - Atualizar apresentação COP30 com seção "Taxonomia BR"
   - Preparar post LinkedIn anunciando integração futura
   - Contatar órgão gestor da Taxonomia para parceria

3. **Proof of Concept** (1 semana)
   - Mapear 1 setor específico (ex: Energia Renovável)
   - Criar script de mapeamento CNAE → Taxonomia para esse setor
   - Avaliar 10 empresas piloto
   - Gerar relatório demonstrativo

4. **Pitch Deck Atualizado** (2 dias)
   - Adicionar slide "Taxonomia BR Integration Roadmap"
   - Destacar first-mover advantage
   - Projeções de mercado atualizadas

---

## 📋 Checklist de Execução

### Sprint 1 (Semana 1-2): Discovery
- [ ] Leitura completa de todos os cadernos setoriais
- [ ] Documento de análise inicial (estrutura, setores, critérios)
- [ ] Mapeamento preliminar de 5 setores prioritários
- [ ] Atualização de materiais de comunicação (COP30, pitch deck)
- [ ] Outreach para órgão gestor da Taxonomia

### Sprint 2 (Semana 3-4): Mapeamento
- [ ] Mapeamento completo CNAE → Taxonomia BR
- [ ] Script automatizado de classificação
- [ ] Análise de impacto quantitativa
- [ ] Design do schema de banco de dados
- [ ] Definição de novos endpoints da API

### Sprint 3 (Semana 5-6): Desenvolvimento
- [ ] Implementação do schema de dados
- [ ] Migração dos dados atuais
- [ ] Desenvolvimento dos endpoints da API
- [ ] Atualização do algoritmo de score verde
- [ ] Testes unitários e de integração

### Sprint 4 (Semana 7-8): Features
- [ ] Dashboard de conformidade (empresas)
- [ ] Painel analítico (admin/B2G)
- [ ] Sistema de relatórios exportáveis
- [ ] Guia de auto-avaliação interativo

### Sprint 5 (Semana 9-10): Conteúdo
- [ ] Materiais educacionais
- [ ] FAQ e documentação
- [ ] Cases de demonstração
- [ ] Preparação de webinar

### Sprint 6 (Semana 11-12): Lançamento
- [ ] Beta test com 10 empresas piloto
- [ ] Ajustes baseados em feedback
- [ ] Press release e comunicação
- [ ] Lançamento oficial

---

## 🚀 Proposta de Ação Imediata

### O que fazer AGORA (próximas 48h):

1. **Você** (Bruno):
   - Compartilhar resumo executivo dos cadernos setoriais
   - Destacar setores prioritários para seu negócio
   - Listar quaisquer contatos no órgão gestor da Taxonomia

2. **Eu** (GitHub Copilot):
   - Criar template de análise para cada caderno setorial
   - Preparar script de extração de dados (se cadernos forem estruturados)
   - Atualizar ROADMAP.md com novo milestone TSB-01

3. **Próxima sessão**:
   - Revisar análise dos cadernos
   - Priorizar setores para mapeamento inicial
   - Definir MVP para POC (Proof of Concept)

---

## 💡 Considerações Finais

Esta é uma **oportunidade única** de transformar Green Jobs Brasil de uma plataforma de empregos para **infraestrutura nacional de taxonomia sustentável**.

**Vantagens do timing**:
- ✅ Taxonomia em fase de consulta pública (ainda podemos influenciar)
- ✅ Mercado sem soluções prontas (first-mover total)
- ✅ COP30 no Brasil (vitrine global)
- ✅ Governo precisará de ferramentas de implementação (B2G acelerado)

**Riscos de NÃO agir rápido**:
- ❌ Concorrentes podem acordar para a oportunidade
- ❌ Perder janela de influenciar a taxonomia via consulta pública
- ❌ Empresas adotarão soluções alternativas (lock-in)

**Minha recomendação**: 
Priorizar TSB-01 sobre P3 (Deploy) temporariamente. A vantagem competitiva da Taxonomia BR é maior que otimizações de infraestrutura. Podemos fazer P3 em paralelo ou após TSB-01 Sprint 1-2.

---

**Próximo passo**: Você me compartilha os insights dos cadernos e começamos a análise técnica?
