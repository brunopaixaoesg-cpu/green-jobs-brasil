# Checklist de Ações Imediatas - Comunicação Estratégica TSB

**Data de início**: 12/11/2025  
**Objetivo**: Posicionar Green Jobs Brasil como primeira plataforma integrada com a Taxonomia Sustentável Brasileira

---

## ✅ FASE 1: MATERIAIS CRIADOS (Concluído)

- [x] Análise completa do Plano de Ação TSB (`TSB_PLANO_DE_ACAO_ANALISE.md`)
- [x] Atualização da apresentação COP30 HTML (seção TSB adicionada)
- [x] Contribuição para consulta pública (40+ páginas, `CONTRIBUICAO_CONSULTA_PUBLICA_TSB.md`)
- [x] Press release oficial (`PRESS_RELEASE_TSB.md`)
- [x] Email de contato estratégico CITSB (`EMAIL_CONTATO_CITSB.md`)
- [x] Mapeamento CNAE TSB vs GJB (`CNAEs_TSB_vs_GJB.csv`)

---

## 📋 FASE 2: AÇÕES IMEDIATAS (Esta Semana)

### Comunicação Digital

- [ ] **Atualizar site institucional**
  - Adicionar badge "🇧🇷 Integrado com a TSB Oficial" no header
  - Criar página `/taxonomia-sustentavel-brasileira`
  - Adicionar seção "TSB" no FAQ

- [ ] **Atualizar apresentação PowerPoint COP30**
  - Adicionar slide "Taxonomia Sustentável Brasileira"
  - Atualizar slide de roadmap (incluir milestone TSB-01)
  - Gerar nova versão do PPT

- [ ] **Post LinkedIn/Redes Sociais** (Rascunho)
  ```
  🇧🇷 ANÚNCIO IMPORTANTE 🌱
  
  A Green Jobs Brasil se torna a PRIMEIRA plataforma integrada 
  com a Taxonomia Sustentável Brasileira oficial!
  
  🎯 O que isso significa?
  ✅ Classificação de empresas nos 11 objetivos da TSB
  ✅ Dashboard de conformidade para os 8 setores prioritários
  ✅ Alinhamento com política pública federal
  ✅ Credibilidade para investidores e reguladores
  
  📊 Impacto:
  • 93.000+ empresas elegíveis
  • 160+ CNAEs mapeados
  • 7M de empregos verdes até 2030
  
  A TSB é um marco para o Brasil. E nós estamos prontos para 
  operacionalizá-la! 🚀
  
  #TaxonomiaSustentavel #TSB #GreenJobsBrasil #COP30
  
  Saiba mais: [link]
  ```

- [ ] **Atualizar GitHub README.md**
  - Adicionar badge TSB
  - Mencionar integração na descrição do projeto
  - Link para documentação TSB

### Contato Institucional

- [ ] **Identificar contatos do CITSB**
  - Pesquisar site do Ministério da Fazenda
  - Identificar coordenadores de GTs setoriais no LinkedIn
  - Localizar email oficial da consulta pública
  - Buscar participantes em eventos sobre a TSB

- [ ] **Enviar email ao CITSB**
  - Revisar e personalizar `EMAIL_CONTATO_CITSB.md`
  - Preparar anexos (slides, planilha CNAE, proposta piloto)
  - Enviar para múltiplos destinatários (CC)
  - Follow-up após 1 semana se sem resposta

- [ ] **Submeter contribuição à consulta pública**
  - Verificar canal oficial de submissão
  - Formatar `CONTRIBUICAO_CONSULTA_PUBLICA_TSB.md` conforme template oficial
  - Anexar evidências (planilhas, documentação técnica)
  - Guardar comprovante de submissão

### Preparação de Materiais

- [ ] **Criar apresentação institucional (15 slides)**
  - Slide 1: Capa Green Jobs Brasil
  - Slide 2: Problema (fragmentação de dados)
  - Slide 3: Solução (infraestrutura de dados)
  - Slide 4: Como funciona (CNAE → ODS → TSB)
  - Slide 5: Números (1.000 empresas, 43 CNAEs)
  - Slide 6: Integração TSB (11 objetivos, 8 setores)
  - Slide 7: Ferramentas (API, dashboard, ETL)
  - Slide 8: Proposta de piloto (Energia + Transporte)
  - Slide 9: Timeline (3-6-12 meses)
  - Slide 10: Impacto esperado (93k empresas, 7M empregos)
  - Slide 11: Modelo de colaboração (co-criação)
  - Slide 12: Equipe e expertise
  - Slide 13: Parceiros e validações
  - Slide 14: Próximos passos
  - Slide 15: Contato

- [ ] **Exportar planilha de 43 CNAEs**
  - Ler `etl/cnae_green_seed.csv`
  - Formatar com colunas: CNAE, Descrição, Categoria GJB, ODS, Scoring, Justificativa, Fontes
  - Salvar como `GJB_CNAEs_Verdes_Atuais.xlsx`

- [ ] **Criar proposta de piloto (5 páginas)**
  - Escopo: 2 setores (Energia D + Transporte H)
  - Amostra: 100 empresas por setor (200 total)
  - Metodologia: Aplicar critérios CS/NPS/SM
  - Timeline: 3 meses
  - Entregáveis: Relatório de aprendizados, sugestões de refinamento
  - Investimento: R$ 50k (subsidizado)

- [ ] **Capturar screenshots do dashboard**
  - Tela inicial (mapa de empresas)
  - Tela de perfil de empresa (score verde, CNAEs, ODS)
  - Tela de listagem de vagas verdes
  - Tela de estatísticas agregadas
  - Salvar em alta resolução (PNG, 1920x1080)

### Pesquisa e Inteligência

- [ ] **Mapear concorrentes/similares**
  - Existe outra plataforma mapeando TSB?
  - Consultorias oferecendo compliance TSB?
  - Ferramentas internacionais adaptáveis ao Brasil?
  - Nossa vantagem competitiva vs. cada uma

- [ ] **Identificar eventos relevantes**
  - Lançamento oficial da TSB (quando?)
  - Eventos do Ministério da Fazenda sobre finanças sustentáveis
  - Fóruns de ESG/sustentabilidade onde apresentar
  - Webinars sobre taxonomia (participar ou organizar?)

- [ ] **Pesquisar financiamento**
  - Editais BNDES para inovação sustentável
  - Embrapii (tecnologia verde)
  - Fundos de impacto (investidores alinhados com ESG)
  - Orçamento do próprio CITSB para ferramentas digitais

---

## 📅 FASE 3: AÇÕES DE CURTO PRAZO (Próximas 2 Semanas)

### Desenvolvimento Técnico

- [ ] **Criar endpoint de API TSB (MVP)**
  - `/api/taxonomia-br/avaliar/{cnpj}` - Avalia conformidade TSB de uma empresa
  - Retorna: Objetivos alinhados (CS), Violações (NPS), Salvaguardas (SM), Score TSB (0-100)
  - Documentar no Swagger/OpenAPI

- [ ] **Protótipo de dashboard TSB**
  - Página `/empresa/{cnpj}/taxonomia-tsb`
  - Visualização dos 11 objetivos (círculo/radar chart)
  - Lista de critérios CS/NPS/SM com status (✅/⚠️/❌)
  - Botão "Exportar Relatório TSB" (gera PDF)

- [ ] **Script de classificação automática TSB**
  - Input: CNAE da empresa
  - Output: Quais objetivos TSB são elegíveis (CS)
  - Lógica inicial: Baseado na análise do Plano de Ação
  - Refinamento futuro: Com critérios detalhados dos cadernos setoriais

### Conteúdo e Educação

- [ ] **Criar FAQ "O que é a TSB?"**
  - 10 perguntas comuns de empresas
  - Linguagem simples (não técnica)
  - Exemplos práticos por setor
  - Publicar no site

- [ ] **Artigo LinkedIn longo-form**
  - Título: "Taxonomia Sustentável Brasileira: O que empresas precisam saber"
  - 1.500-2.000 palavras
  - SEO: Palavras-chave TSB, taxonomia sustentável, finanças verdes Brasil
  - Call-to-action: Acessar nossa plataforma

- [ ] **Vídeo explicativo (3-5 min)**
  - O que é a TSB?
  - Por que empresas devem se importar?
  - Como a Green Jobs Brasil ajuda?
  - Publicar no YouTube/LinkedIn

### Networking e Parcerias

- [ ] **Listar parceiros potenciais**
  - **Academia**: USP, FGV, Unicamp (pesquisas ESG)
  - **ONGs**: TNC, WWF, Imaflora (validação de critérios)
  - **Governo**: BNDES, Sebrae (difusão para PMEs)
  - **Setor privado**: Febraban, CNI (adoção corporativa)

- [ ] **Agendar reuniões exploratórias**
  - 1 reunião por semana nas próximas 4 semanas
  - Pitch: "Somos a ferramenta digital da TSB"
  - Perguntar: "Como vocês planejam usar a TSB? Podemos colaborar?"

- [ ] **Participar de grupos/fóruns**
  - LinkedIn: Procurar grupos sobre ESG, finanças sustentáveis Brasil
  - Telegram/WhatsApp: Comunidades de sustentabilidade
  - Eventos: Inscrever-se como palestrante em webinars

---

## 🎯 FASE 4: AÇÕES DE MÉDIO PRAZO (Próximo Mês)

### Produto e Tecnologia

- [ ] **Dashboard TSB completo**
  - Auto-avaliação guiada (wizard)
  - Upload de evidências (certificados, licenças)
  - Cálculo automático de score TSB
  - Relatório exportável (PDF branded)

- [ ] **Integração com bases governamentais**
  - IBAMA (áreas embargadas) para critério NPS
  - MTE (lista suja trabalho escravo) para SM
  - ICMBio (UCs) para critério NPS biodiversidade
  - APIs disponíveis vs. scraping vs. datasets públicos

- [ ] **Sistema de versionamento da taxonomia**
  - Cada versão da TSB (v1.0, v1.1, v2.0) salva separadamente
  - Empresas podem ver score em diferentes versões
  - Rastreabilidade: "Em TSB v1.0 você era Verde, em v1.1 é Transição" (com explicação)

### Comercial e Marketing

- [ ] **Criar página de produto "TSB Compliance Suite"**
  - Tier Gratuito: Auto-avaliação básica
  - Tier Profissional: Relatórios customizados, consultoria
  - Tier Enterprise: Multi-unidades, API integration
  - Precificação: R$ 0 / R$ 500 / R$ 2.000 / R$ 10.000+ /mês

- [ ] **Material de vendas B2G**
  - Pitch deck específico para governos
  - Cases de uso: Compras públicas sustentáveis, monitoramento NDC
  - ROI: Economia em auditoria manual, transparência
  - Contrato-tipo para estados/municípios

- [ ] **Webinar "Taxonomia TSB na Prática"**
  - Público: Empresas, consultores, investidores
  - Conteúdo: Explicar TSB + demonstrar nossa ferramenta
  - 1 hora (30 min apresentação + 30 min Q&A)
  - Captar leads (inscritos = potenciais clientes)

### Dados e Expansão

- [ ] **Mapear CNAEs dos 8 setores TSB**
  - Setor A: Listar todos os CNAEs de agricultura/pecuária/florestal/pesca
  - Setor B: CNAEs de mineração (com foco em minerais estratégicos)
  - Setor C: Indústria de transformação (8 subsegmentos)
  - Setor D: Energia (já temos base)
  - Setor E: Água/esgoto/resíduos
  - Setor F: Construção (HIS + infraestrutura)
  - Setor H: Transporte (7 modais)
  - Transversal: Turismo + TIC + Planejamento Urbano
  - **Total estimado**: 160+ CNAEs novos

- [ ] **Importar empresas dos setores TSB**
  - Consultar API Receita Federal com CNAEs identificados
  - Filtrar empresas ativas
  - Salvar em database com flag `tsb_setor`
  - Meta: Expandir de 1.000 para 10.000 empresas

- [ ] **Criar dataset público "Empresas TSB Brasil"**
  - CSV/JSON com: CNPJ, Razão Social, CNAE, Setor TSB, Score TSB
  - Licença: Creative Commons (dados abertos)
  - Publicar no GitHub + Kaggle + Brasil.io
  - PR: "Primeiro dataset público de empresas TSB no Brasil"

---

## 📊 FASE 5: MÉTRICAS DE SUCESSO (Acompanhamento Contínuo)

### KPIs de Comunicação

- [ ] **Alcance do press release**
  - Quantos veículos republicaram?
  - Menções em portais de sustentabilidade/finanças?
  - Shares em redes sociais

- [ ] **Engajamento digital**
  - Visualizações da página `/taxonomia-sustentavel-brasileira`
  - Downloads da contribuição para consulta pública
  - Inscritos no webinar TSB

- [ ] **Networking institucional**
  - Resposta do CITSB ao email? (sim/não)
  - Reuniões agendadas com GTs setoriais? (número)
  - Convites para eventos oficiais sobre TSB? (sim/não)

### KPIs de Produto

- [ ] **Adoção do dashboard TSB**
  - Empresas usando auto-avaliação (número)
  - Relatórios TSB gerados (número)
  - Conversão para tier pago (%)

- [ ] **Qualidade dos dados**
  - CNAEs mapeados (meta: 160+)
  - Empresas classificadas (meta: 10.000+)
  - Precisão da classificação (auditoria manual de amostra)

### KPIs de Impacto

- [ ] **Legitimidade institucional**
  - Mencionados em documentos oficiais do CITSB? (sim/não)
  - Parceria formalizada? (termo de cooperação)
  - Credenciamento como ferramenta oficial? (sim/não)

- [ ] **Tração comercial**
  - Clientes pagantes TSB Compliance Suite (número)
  - Contratos B2G (número)
  - ARR (Annual Recurring Revenue) de produtos TSB

- [ ] **Reconhecimento de mercado**
  - Prêmios/menções em ESG/inovação sustentável
  - Citações em pesquisas acadêmicas sobre TSB
  - Convites para palestras/painéis

---

## 🚨 RISCOS E MITIGAÇÕES

### Risco 1: CITSB não responde ou não tem interesse em parceria

**Probabilidade**: Média  
**Impacto**: Alto

**Mitigação**:
- Plano B: Implementar TSB independentemente (com base em documentos públicos)
- Seguir contribuindo para consultas públicas (posicionamento de longo prazo)
- Buscar parcerias alternativas (GTs setoriais específicos, BNDES, universidades)
- Comunicar mesmo assim como "alinhado com TSB" (não "oficial")

### Risco 2: Concorrente lança solução TSB antes de nós

**Probabilidade**: Baixa (6 meses de vantagem estimada)  
**Impacto**: Médio

**Mitigação**:
- Acelerar desenvolvimento (priorizar MVP funcional vs. perfeito)
- Comunicação agressiva ("primeira plataforma integrada")
- Diferenciação: API aberta + dados públicos (vs. soluções fechadas)
- Foco em qualidade e profundidade (vs. superficialidade)

### Risco 3: TSB muda significativamente na versão final

**Probabilidade**: Média  
**Impacto**: Médio

**Mitigação**:
- Sistema de versionamento (fácil atualizar quando TSB v1.0 oficial sair)
- Arquitetura modular (critérios em JSON configurável, não hardcoded)
- Comunicar como "baseado no Plano de Ação" (deixar claro que é preliminar)
- Participar ativamente da consulta pública (influenciar resultado final)

### Risco 4: Baixa adoção de empresas (produto não tem demanda)

**Probabilidade**: Baixa (TSB será obrigatória para muitas empresas)  
**Impacto**: Alto

**Mitigação**:
- Tier gratuito robusto (reduzir barreira de entrada)
- Parcerias com associações setoriais (Febraban, CNI) para difusão
- Educar mercado (webinars, conteúdo, eventos)
- Foco inicial em early adopters (grandes empresas com metas ESG)

---

## ✅ CHECKLIST FINAL (Antes de Executar)

Antes de começar, revisar:

- [ ] Todos os documentos estão grammaticalmente corretos e profissionais?
- [ ] Informações sensíveis (email, telefone, CNPJ) estão corretas ou marcadas como [a preencher]?
- [ ] Links para site, API, GitHub estão funcionando?
- [ ] Anexos mencionados (slides, planilhas, PDFs) estão criados e prontos?
- [ ] Tom de comunicação é profissional mas não subserviente (parceria de igual para igual)?
- [ ] Oferta de colaboração é concreta e tangível (não vaga)?
- [ ] Há call-to-action claro em cada material (o que queremos que façam)?

---

**Responsável**: Bruno Paixão  
**Data de criação**: 12/11/2025  
**Última atualização**: 12/11/2025  
**Status**: Em execução

**Próxima revisão**: Semanal (toda segunda-feira)  
**Formato de reporte**: Marcar [x] ao concluir cada item + adicionar data de conclusão

---

**INÍCIO DA EXECUÇÃO**: AGORA! 🚀
