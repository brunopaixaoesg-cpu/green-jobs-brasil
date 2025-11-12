# Guia Prático - Análise da Taxonomia Sustentável Brasileira

**Objetivo**: Extrair dados estruturados dos cadernos setoriais para integração no Green Jobs Brasil

---

## 🚀 Como Começar (Passo a Passo)

### Passo 1: Organizar os Cadernos (5 minutos)

1. **Baixe ou copie** todos os cadernos setoriais para:
   ```
   c:\Users\Bruno\Empresas Verdes\data\taxonomia_br\cadernos\
   ```

2. **Renomeie** os arquivos de forma padronizada:
   ```
   taxonomia_br_energia.pdf
   taxonomia_br_transporte.pdf
   taxonomia_br_construcao.pdf
   etc.
   ```

3. **Liste** os setores disponíveis em um arquivo:
   ```
   data/taxonomia_br/SETORES_DISPONIVEIS.txt
   ```

---

### Passo 2: Escolher o Setor Prioritário (10 minutos)

**Critérios para priorização**:
1. **Representatividade**: Setores com mais empresas/empregos no Brasil
2. **Facilidade**: Setores com critérios mais claros e objetivos
3. **Alinhamento**: Setores que já temos CNAEs mapeados (43 atuais)

**Sugestão de ordem** (baseado em experiência internacional):

1. **ENERGIA RENOVÁVEL** ⭐⭐⭐
   - Alta representatividade no Brasil (hidro, solar, eólica, biomassa)
   - Critérios bem estabelecidos (ex: EU Taxonomy)
   - Já temos CNAEs mapeados (3511, 3512, 3513, etc.)
   - Alto potencial de empregos verdes

2. **CONSTRUÇÃO SUSTENTÁVEL** ⭐⭐
   - Setor grande (muitas empresas)
   - Critérios claros (certificações LEED, AQUA)
   - Potencial de transição (retrofit de edifícios)

3. **TRANSPORTE LIMPO** ⭐⭐
   - Mobilidade elétrica em crescimento
   - Transporte público sustentável
   - Logística verde

4. **AGROPECUÁRIA SUSTENTÁVEL** ⭐⭐⭐
   - Específico do Brasil (bioeconomia, amazônia)
   - Potencial enorme (agro verde)
   - Complexo (muitos critérios)

5. **GESTÃO DE RESÍDUOS E ECONOMIA CIRCULAR** ⭐
   - Reciclagem, compostagem, valorização
   - Já mapeado (CNAEs 38xx)

**Escolha**: _________________________

---

### Passo 3: Análise Interativa (30-60 minutos por setor)

**Execute o script de análise interativa**:

```powershell
cd c:\Users\Bruno\Empresas Verdes
python scripts\analise\extrair_taxonomia_br.py --setor "Energia"
```

O script vai fazer perguntas e você responde baseado no caderno:

#### 3.1 Perguntas Básicas
- Nome do caderno
- Versão
- Data de publicação

#### 3.2 Objetivos Ambientais
Quais dos 6 objetivos o setor atende? (marcar s/n)

#### 3.3 Atividades Elegíveis
Para cada atividade identificada no caderno:
- Nome (ex: "Geração de energia solar fotovoltaica")
- Código (se houver)
- Categoria (Verde/Transição/Não-elegível)
- Descrição

#### 3.4 Mapeamento CNAE
Para cada atividade, liste CNAEs relacionados:
- Código CNAE
- Tipo de alinhamento (Core/Adjacent/Transição)
- Descrição do CNAE

#### 3.5 Critérios Técnicos
- Tipo (Quantitativo/Qualitativo/Misto)
- Há thresholds numéricos?
- Exemplos de thresholds

#### 3.6 Estimativas
- Empresas potenciais
- Empregos potenciais

#### 3.7 Insights
Observações importantes (texto livre)

**Resultado**: O script gera automaticamente:
- ✅ `data/taxonomia_br/analises/energia.json` (dados estruturados)
- ✅ `data/taxonomia_br/analises/energia_relatorio.md` (relatório legível)
- ✅ `data/taxonomia_br/extratos/energia_atividades.csv` (atividades)
- ✅ `data/taxonomia_br/mapeamentos/energia_cnae_mapping.csv` (mapeamentos)

---

### Passo 4: Repetir para Outros Setores (conforme tempo disponível)

Execute para cada setor prioritário:
```powershell
python scripts\analise\extrair_taxonomia_br.py --setor "Transporte"
python scripts\analise\extrair_taxonomia_br.py --setor "Construcao"
# etc.
```

---

### Passo 5: Consolidar Análises (5 minutos)

Depois de analisar 2-3 setores, consolide:

```powershell
python scripts\analise\extrair_taxonomia_br.py --consolidar
```

**Resultado**:
- ✅ `data/taxonomia_br/analises/CONSOLIDADO.md` (visão geral)
- ✅ `data/taxonomia_br/analises/analise_consolidada.json` (dados agregados)

Mostra:
- Total de setores analisados
- Total de atividades elegíveis
- Total de CNAEs mapeados
- Estimativa de empresas e empregos

---

## 📊 O Que Fazer com os Dados Extraídos

### Curto Prazo (1-2 semanas)

1. **Atualizar CNAEs Verdes**
   - Adicionar novos CNAEs identificados
   - Reclassificar CNAEs existentes (Core/Adjacent/Secondary)
   - Atualizar arquivo `etl/cnae_green_seed.csv`

2. **Recalcular Scores**
   - Implementar novo algoritmo de score (Taxonomia BR 40% + CNAE 30% + ODS 20% + Indicadores 10%)
   - Executar ETL com novos scores
   - Validar resultados

3. **Criar POC (Proof of Concept)**
   - Dashboard de conformidade para 1 setor
   - Endpoint de API para consulta de conformidade
   - Relatório exportável (PDF)

### Médio Prazo (3-4 semanas)

4. **Desenvolver Features Completas**
   - API endpoints para Taxonomia BR
   - Dashboard de conformidade para empresas
   - Painel analítico para B2G

5. **Materiais de Comunicação**
   - Atualizar apresentação COP30
   - Criar guia educacional sobre Taxonomia BR
   - Preparar cases de demonstração

6. **Lançamento Beta**
   - Convidar 10 empresas piloto
   - Coletar feedback
   - Ajustar produto

---

## 🎯 Exemplo Prático - Setor Energia

**Contexto**: Você está analisando o caderno de "Energia Renovável"

### Entrada (o que você lê no caderno):

**Atividade 1**: Geração de energia solar fotovoltaica
- Categoria: Verde
- Critério: Geração de eletricidade a partir de energia solar fotovoltaica
- Threshold: Não aplicável (atividade intrinsecamente verde)

**Atividade 2**: Fabricação de equipamentos para energia solar
- Categoria: Verde
- Critério: Fabricação de painéis fotovoltaicos, inversores, etc.

### Saída (o que o script gera):

**JSON**:
```json
{
  "setor": "Energia",
  "atividades": [
    {
      "nome": "Geração de energia solar fotovoltaica",
      "codigo": "TAXBR-ENE-001",
      "categoria": "Verde",
      "descricao": "Geração de eletricidade a partir de energia solar fotovoltaica"
    },
    {
      "nome": "Fabricação de equipamentos para energia solar",
      "codigo": "TAXBR-ENE-002",
      "categoria": "Verde",
      "descricao": "Fabricação de painéis, inversores e componentes"
    }
  ],
  "cnaes_mapeados": [
    {
      "cnae": "3511-5/01",
      "atividade": "Geração de energia solar fotovoltaica",
      "tipo_alinhamento": "Core",
      "descricao_cnae": "Geração de energia elétrica - solar"
    },
    {
      "cnae": "2710-4/01",
      "atividade": "Fabricação de equipamentos para energia solar",
      "tipo_alinhamento": "Core",
      "descricao_cnae": "Fabricação de geradores de corrente contínua e alternada, peças e acessórios"
    }
  ]
}
```

**CSV de mapeamento**:
```csv
cnae,atividade,tipo_alinhamento,descricao_cnae
3511-5/01,Geração de energia solar fotovoltaica,Core,Geração de energia elétrica - solar
2710-4/01,Fabricação de equipamentos para energia solar,Core,Fabricação de geradores de corrente contínua e alternada
```

**Relatório MD**:
```markdown
# Análise - Setor Energia

## Atividades Elegíveis (2)

### Geração de energia solar fotovoltaica
- **Categoria**: Verde
- **Código**: TAXBR-ENE-001
- **Descrição**: Geração de eletricidade a partir de energia solar fotovoltaica

### Fabricação de equipamentos para energia solar
- **Categoria**: Verde
- **Código**: TAXBR-ENE-002
- **Descrição**: Fabricação de painéis, inversores e componentes

## Mapeamentos CNAE (2)

| CNAE | Atividade | Alinhamento | Descrição |
|------|-----------|-------------|-----------|
| 3511-5/01 | Geração de energia solar fotovoltaica | Core | Geração de energia elétrica - solar |
| 2710-4/01 | Fabricação de equipamentos para energia solar | Core | Fabricação de geradores |
```

---

## 💡 Dicas Importantes

### Durante a Análise

1. **Seja consistente** nos nomes (use exatamente o que está no caderno)
2. **Documente dúvidas** nos insights (para esclarecer depois)
3. **Seja conservador** nas estimativas (melhor subestimar)
4. **Foque na qualidade** (melhor 1 setor bem analisado que 5 superficiais)

### Mapeamento CNAE

- **Core**: CNAE 100% alinhado com a atividade da taxonomia
- **Adjacent**: CNAE parcialmente alinhado (ex: pode incluir atividades não-verdes também)
- **Transição**: CNAE que pode se tornar verde com adaptações

### Critérios Técnicos

Se houver thresholds numéricos (ex: "<100gCO2/kWh"), documente EXATAMENTE como está escrito. Será crucial para automação futura.

---

## 📞 Próximos Passos

Depois de completar a análise de 2-3 setores prioritários:

1. **Revisão comigo** (GitHub Copilot):
   - Validar estrutura dos dados
   - Identificar gaps ou inconsistências
   - Priorizar setores para POC

2. **Desenvolvimento do POC**:
   - Implementar dashboard de conformidade
   - Testar com empresas reais
   - Validar algoritmo de scoring

3. **Comunicação Estratégica**:
   - Atualizar materiais COP30
   - Preparar outreach para órgão gestor
   - Iniciar conversas com primeiros clientes B2B/B2G

---

## ✅ Checklist Rápido

- [ ] Cadernos organizados em `data/taxonomia_br/cadernos/`
- [ ] Setor prioritário escolhido
- [ ] Script de análise testado (`python scripts\analise\extrair_taxonomia_br.py --setor "Teste"`)
- [ ] Primeiro setor analisado completamente
- [ ] Arquivos JSON/CSV/MD gerados e revisados
- [ ] Segundo setor analisado (se tempo permitir)
- [ ] Consolidação executada
- [ ] Relatório consolidado revisado
- [ ] Próximos passos definidos

---

**Dúvidas?** Pergunte! Estou aqui para ajudar em cada etapa. 🚀
