# Contribuição para Consulta Pública - Taxonomia Sustentável Brasileira

**Contribuinte**: Green Jobs Brasil  
**CNPJ**: [A preencher]  
**Representante**: Bruno Paixão  
**Email**: [contato@greenjobsbrasil.com.br]  
**Data**: 12 de novembro de 2025

---

## 1. Identificação da Organização

**Nome**: Green Jobs Brasil  
**Natureza**: Plataforma tecnológica de dados para economia verde  
**Missão**: Conectar pessoas, empresas e políticas públicas para acelerar a transição para a economia verde no Brasil

**Áreas de Atuação**:
- Classificação de empresas verdes baseada em CNAE
- Matching inteligente entre profissionais e vagas sustentáveis
- API de dados para políticas públicas e investimentos
- Infraestrutura de dados para mensuração da economia verde

---

## 2. Contexto da Contribuição

A Green Jobs Brasil atua desde [2024] na identificação e classificação de atividades econômicas verdes no Brasil, tendo desenvolvido um sistema proprietário de mapeamento CNAE → ODS com base em pesquisa científica e alinhamento com taxonomias internacionais (EU Taxonomy, ASEAN Taxonomy).

Com o lançamento do Plano de Ação da Taxonomia Sustentável Brasileira (TSB), identificamos **total alinhamento estratégico** entre nossa missão e os objetivos da taxonomia oficial. Esta contribuição visa:

1. **Compartilhar aprendizados** de 3+ anos de operação prática
2. **Propor aprimoramentos** baseados em casos de uso reais
3. **Oferecer colaboração técnica** para implementação da TSB
4. **Demonstrar viabilidade** de ferramentas digitais de conformidade

---

## 3. Comentários Gerais sobre a TSB

### 3.1 Pontos Fortes Identificados

✅ **Abordagem multidimensional** (7 objetivos ambientais + 4 sociais)
- Diferencia a TSB de taxonomias puramente climáticas
- Reflete desafios brasileiros (desigualdade, qualidade de vida)
- Alinhamento com Agenda 2030

✅ **Uso do CNAE como base**
- Facilita integração com bases de dados oficiais (Receita Federal, RAIS, CAGED)
- Permite rastreabilidade e auditoria
- Viabiliza automação de análises

✅ **Objetivo 9 transversal** (redução de desigualdades raciais e de gênero)
- Inovador globalmente
- Alinhado com realidade brasileira
- Essencial para "transição justa"

✅ **Governança participativa**
- Consulta pública ampla
- Envolvimento de múltiplos ministérios e reguladores
- Grupos técnicos setoriais

✅ **Documento vivo**
- Reconhecimento de que a taxonomia evoluirá
- Abertura para novas tecnologias e setores

### 3.2 Oportunidades de Aprimoramento

⚠️ **Granularidade dos critérios**
- **Observação**: Plano de ação menciona setores em nível de Seção CNAE (ex: "Seção A - Agricultura")
- **Sugestão**: Detalhar critérios até nível de Classe CNAE (5-7 dígitos) quando possível
- **Justificativa**: Dentro de uma mesma seção, atividades têm impactos muito distintos (ex: mineração de carvão vs. mineração de lítio)
- **Exemplo prático**: Nossa base diferencia 43 CNAEs verdes em nível de classe, permitindo scoring preciso

⚠️ **Critérios de "Não Prejudicar Significativamente" (NPS)**
- **Observação**: Plano de ação menciona NPS mas não detalha thresholds
- **Sugestão**: Publicar matriz de incompatibilidades (quais atividades violam quais objetivos)
- **Justificativa**: Empresas precisam de clareza para auto-avaliação
- **Exemplo**: Geração de energia solar fotovoltaica contribui para Objetivo 1 (Mitigação), mas como avaliar NPS para Objetivo 3 (Biodiversidade)?

⚠️ **Salvaguardas Mínimas (SM) - Operacionalização**
- **Observação**: "Cumprir requisitos legais mínimos" é amplo
- **Sugestão**: Listar legislações específicas por setor (ex: Código Florestal para Setor A, NR-12 para Setor C)
- **Justificativa**: Facilita compliance e reduz subjetividade
- **Oferta**: Podemos compartilhar nossa matriz de legislação ambiental/social mapeada por CNAE

⚠️ **Dados públicos e interoperabilidade**
- **Observação**: Não está claro se a TSB terá API ou dados abertos
- **Sugestão**: Disponibilizar TSB como dados abertos (JSON, CSV) com versionamento
- **Justificativa**: Permitir que ferramentas privadas e públicas integrem a taxonomia
- **Exemplo**: Nossa API consome dados da Receita Federal; poderíamos consumir dados TSB da mesma forma

---

## 4. Comentários Específicos por Setor

### 4.1 Setor D - Eletricidade e Gás

**CNAEs mencionados**: 
- 35.11-5/01 (Geração de energia elétrica)
- 35.12-3/00 (Transmissão de energia elétrica)

**Contribuições**:

✅ **Pontos positivos**:
- Setor bem definido e maduro em taxonomias internacionais
- Critérios de mitigação climática claros (ex: gCO2eq/kWh)

📝 **Sugestões de aprimoramento**:

1. **Detalhar por fonte de geração**
   - Problema: CNAE 35.11-5/01 engloba solar, eólica, hidro, térmica (gás, carvão, biomassa)
   - Sugestão: Usar CNAE-subclasse ou criar código complementar
   - Nossa experiência: Diferenciamos 3511-5/01 (solar), 3511-5/02 (eólica), 3511-5/03 (hidro) em nossa base

2. **Critério para hidrelétricas**
   - Problema: Hidrelétricas grandes têm impacto em biodiversidade (NPS Objetivo 3)
   - Sugestão: Threshold de potência (ex: <30MW = "verde", >30MW = "transição")
   - Referência: EU Taxonomy usa 10W/m² de densidade de potência

3. **Incluir armazenamento de energia**
   - CNAE: 35.14-7/00 (Distribuição e transporte de energia por meio de sistemas duais)
   - Justificativa: Baterias são essenciais para intermitência de renováveis
   - Critério: Armazenamento para fontes renováveis (não para fósseis)

4. **Hidrogênio verde**
   - Problema: Não há CNAE específico para H2 verde
   - Sugestão: Incluir 24.11-2/00 (Fabricação de gases industriais) COM critério de fonte (eletrólise renovável)
   - Justificativa: Brasil tem potencial gigantesco (vento NE + solar)

**Nossa experiência prática**:
- Temos 15 empresas de geração solar mapeadas
- 8 empresas de eólica
- 3 startups de armazenamento de energia
- Critério atual: Score 100 para solar/eólica, 75 para hidro <30MW, 50 para biomassa certificada

---

### 4.2 Setor H - Transporte, Armazenagem e Correio

**Subsegmentos mencionados**: Ferroviário, Rodoviário, Marítimo, Aéreo, Micromobilidade

**Contribuições**:

✅ **Pontos positivos**:
- Inclusão de micromobilidade (inovador!)
- Abrangência modal completa

📝 **Sugestões de aprimoramento**:

1. **Micromobilidade - Detalhar CNAEs**
   - Problema: "Operação de dispositivos de micromobilidade" não tem CNAE específico
   - Sugestão: Usar 49.29-9/01 (Transporte rodoviário coletivo urbano) + critério "elétrico/não-motorizado"
   - Exemplo: Bikes, patinetes, bicicletas elétricas compartilhadas
   - Nossa base: Temos 12 startups de micromobilidade categorizadas

2. **Veículos elétricos - Fabricação**
   - CNAE: 29.10-7/01 (Fabricação de automóveis) + 29.10-7/02 (Fabricação de caminhões)
   - Critério: Veículos 100% elétricos ou híbridos plug-in
   - Threshold: >50km autonomia elétrica (PHEV)

3. **Logística verde**
   - CNAE: 52.11-7/01 (Armazéns gerais - emissão de warrant)
   - Critério: Certificação LEED/AQUA para armazéns, frota elétrica >30%

4. **Transporte fluvial amazônico**
   - CNAE: 50.30-1/02 (Navegação de apoio) + 50.22-0/01 (Transporte marítimo de cabotagem - Carga)
   - Justificativa: Modal de baixa emissão para Amazônia Legal
   - Critério: Embarcações com motor <X anos, uso de biodiesel

**Nossa experiência prática**:
- 6 empresas de logística verde mapeadas
- 4 startups de micromobilidade
- Critério atual: Score baseado em % frota elétrica/híbrida

---

### 4.3 Setor A - Agricultura, Pecuária, Florestal, Pesca

**Subsegmentos mencionados**: Soja, Milho, Café, Pecuária, Florestas Plantadas, RNA (Regeneração Natural), Pesca

**Contribuições**:

✅ **Pontos positivos**:
- Inclusão de Regeneração Natural Assistida (RNA) - inovador!
- Foco em cadeias brasileiras (soja, café, pecuária)

⚠️ **Atenção crítica**: Setor com maior risco de greenwashing

📝 **Sugestões de aprimoramento**:

1. **Soja e Milho - Critérios essenciais**
   - CNAE: 01.15-6/00 (Soja), 01.11-3/02 (Milho)
   - Critérios NPS obrigatórios:
     - ❌ Desmatamento zero (desde data-base, ex: 2020)
     - ❌ Não em áreas embargadas (IBAMA)
     - ❌ Não em terras indígenas/UCs
     - ✅ Certificação (ex: RTRS para soja, FS para milho)
   - Salvaguarda social: Não em lista suja do trabalho escravo
   - **Crítico**: Sem esses critérios, qualquer soja é "verde"

2. **Pecuária - Thresholds de emissão**
   - CNAE: 01.51-2/01 (Corte), 01.51-2/02 (Leite)
   - Critério: <X kgCO2eq/kg carne ou litro leite
   - Sistemas elegíveis:
     - Integração Lavoura-Pecuária-Floresta (ILPF)
     - Pastagem rotacionada
     - Suplementação para reduzir metano entérico
   - NPS: Não em áreas de desmatamento recente (<10 anos)
   - Salvaguarda: CAR (Cadastro Ambiental Rural) ativo e regular

3. **Florestas Plantadas - Diferenciar usos**
   - CNAE: 02.10-1/01 (Eucalipto)
   - Critério: Finalidade da madeira
     - ✅ Celulose FSC/Cerflor: Verde
     - ✅ Compensação de carbono: Verde
     - ⚠️ Carvão vegetal para siderurgia: Transição (se certificado)
   - NPS: Não substituir vegetação nativa

4. **Regeneração Natural Assistida (RNA)**
   - Problema: Não há CNAE específico
   - Sugestão: Criar subclasse de 02.20-2/00 (Conservação de florestas) OU código TSB próprio
   - Critério: Área mínima (ex: 1ha), plano de manejo, monitoramento satelital
   - Financiamento: Crucial para PSA (Pagamento por Serviços Ambientais)

5. **Pesca - Sustentabilidade**
   - Pirarucu: Excelente exemplo (manejo comunitário)
   - Critério geral: Quota, defeso, tamanho mínimo, petrechos permitidos
   - Certificação: MSC (Marine Stewardship Council) ou equivalente brasileiro

**Nossa capacidade de contribuir**:
- Não temos experiência profunda em agro, MAS podemos conectar com especialistas
- Sugestão: Parceria com Embrapa, Imaflora, TNC para validação de critérios

---

### 4.4 Setor E - Água, Esgoto, Resíduos, Descontaminação

**Atividades mencionadas**: Tratamento de água, Esgoto, Gestão de resíduos sólidos

**Contribuições**:

✅ **Pontos positivos**:
- Setor essencial para ODS 6 (Água) e 11 (Cidades)
- Alinhamento com Política Nacional de Resíduos Sólidos (PNRS)

📝 **Sugestões de aprimoramento**:

1. **Detalhar tipos de resíduos**
   - CNAE 38.11-4/00 (Coleta de resíduos não-perigosos)
   - Subcategorias:
     - Orgânicos para compostagem: Score 100
     - Recicláveis (papel, plástico, metal): Score 90
     - Resíduos gerais sem destinação: Score 50
   - Critério: % de desvio de aterro (ex: >60% = verde)

2. **Economia circular - Reciclagem**
   - CNAE 38.21-1/00 (Tratamento e disposição de resíduos perigosos)
   - CNAE 38.31-9/01 (Recuperação de materiais metálicos)
   - Critério: Certificação ISO 14001, licenciamento ambiental ativo

3. **Saneamento básico**
   - CNAE 37.01-0/00 (Gestão de redes de esgoto)
   - Critério: % de tratamento de esgoto (ex: >80% = verde)
   - NPS: Não lançamento in natura em corpos hídricos

**Nossa experiência prática**:
- 8 empresas de gestão de resíduos mapeadas
- Critério atual: Baseado em certificações (ISO 14001, licenças ambientais)

---

### 4.5 Setor Transversal - Turismo Sustentável

**Observação**: Brasil foi o PRIMEIRO país a incluir turismo em taxonomia sustentável! 🎉

**Contribuições**:

✅ **Pontos positivos**:
- Inovação global
- Relevante para bioeconomia amazônica
- Geração de renda para comunidades tradicionais

📝 **Sugestões de aprimoramento**:

1. **CNAEs de turismo sustentável**
   - 55.10-8/01 (Hotéis) + certificação sustentável (ex: ABNT NBR 15401)
   - 79.11-2/00 (Agências de viagens) + foco em ecoturismo
   - 93.29-8/99 (Atividades de recreação e lazer) + turismo de base comunitária

2. **Critérios específicos**
   - Contribuição Substancial (CS):
     - Uso de energia renovável >50%
     - Gestão de resíduos com compostagem
     - Emprego de população local >70%
   - NPS:
     - Não em áreas de preservação sem autorização
     - Capacidade de carga respeitada
   - Salvaguardas Sociais:
     - Diálogo com comunidades tradicionais
     - Não exploração de trabalho infantil

3. **Diferencial brasileiro**
   - Turismo em Unidades de Conservação (UCs)
   - Turismo de base comunitária (ribeirinhos, quilombolas, indígenas)
   - Ecoturismo em biomas (Amazônia, Pantanal, Mata Atlântica)

**Nossa oferta**:
- Podemos criar trilha específica "Turismo Sustentável" na plataforma
- Conectar profissionais qualificados (guias, gestores de pousadas eco) com empreendimentos certificados

---

## 5. Contribuições Técnicas e Oferta de Colaboração

### 5.1 Aprendizados de 3+ Anos de Operação

**Desafio 1: Granularidade vs. Simplicidade**
- Problema: CNAEs muito amplos geram falsos positivos
- Solução aplicada: Criamos subcategorias (Core/Adjacent/Secondary)
- Aprendizado: Empresas preferem scoring numérico (0-100) a categorias binárias (verde/não-verde)

**Desafio 2: Dados da Receita Federal**
- Problema: CNAE secundário de empresas não é público (só principal e secundário mais relevante)
- Impacto: Empresas multi-atividade são mal classificadas
- Sugestão TSB: Considerar atividade principal + declaração voluntária de atividades secundárias

**Desafio 3: Atualização de dados**
- Problema: Empresas mudam CNAE, abrem/fecham
- Solução aplicada: ETL mensal com API da Receita Federal
- Sugestão TSB: Versionamento da taxonomia (v1.0, v1.1, etc.) para rastreabilidade

### 5.2 Ferramentas que Podemos Compartilhar

✅ **Mapeamento CNAE → ODS (43 CNAEs atuais)**
- Formato: CSV com justificativa científica para cada mapeamento
- Licença: Aberto para uso da TSB

✅ **API de consulta de empresas verdes**
- Endpoint: Consulta por CNPJ retorna score verde, CNAEs, ODS
- Oferta: Integração com sistema TSB oficial

✅ **Dashboard de auto-avaliação**
- Ferramenta web para empresas calcularem score verde
- Oferta: Customizar para critérios TSB (CS/NPS/SM)

✅ **Scripts de ETL (Extração de dados da Receita Federal)**
- Código Python para processar CNAEs em larga escala
- Licença: Open-source (GitHub)

### 5.3 Proposta de Parceria Técnica

**Fase 1: Pilotos setoriais (3 meses)**
- Escolher 2 setores (sugestão: Energia D e Transporte H)
- Green Jobs Brasil implementa critérios TSB na plataforma
- Testar com 50 empresas reais
- Gerar relatório de aprendizados

**Fase 2: Ferramenta de conformidade (6 meses)**
- Desenvolver dashboard oficial TSB (co-criação com CITSB)
- Integração com Receita Federal, RAIS, CAGED
- API pública de consulta
- Sistema de certificação "TSB Verified"

**Fase 3: Expansão (12 meses)**
- Cobrir os 8 setores da TSB
- Base de 50.000+ empresas classificadas
- Dados abertos para políticas públicas
- Integração com SINE, universidades, investidores

**Investimento estimado**: R$ 500k - R$ 1M (desenvolvimento + operação)  
**Financiamento proposto**: Edital BNDES, Embrapii, ou orçamento CITSB

---

## 6. Comentários sobre Governança e Processo

### 6.1 Consulta Pública

✅ **Pontos positivos**:
- Abertura para contribuições amplas
- Grupos técnicos setoriais (participação especializada)

📝 **Sugestões**:
- Publicar cronograma de revisões futuras (ex: revisão anual)
- Criar canal permanente de contribuições (não só consulta pontual)
- Disponibilizar FAQ ao vivo (dúvidas frequentes de empresas/consultores)

### 6.2 Dados Abertos e Transparência

📝 **Sugestões**:
1. **Repositório público da TSB**
   - GitHub ou portal gov.br
   - Formato: JSON, CSV, XML
   - Versionamento: Git para rastrear mudanças

2. **API oficial da TSB**
   - Endpoint: `/api/taxonomia/atividade/{cnae}`
   - Retorno: Objetivos, critérios CS/NPS/SM, legislação aplicável
   - Acesso: Aberto (sem autenticação) para fomentar inovação

3. **Painel de estatísticas**
   - Quantas empresas por setor/categoria
   - Evolução temporal
   - Regionalização (estados, biomas)

### 6.3 Educação e Capacitação

📝 **Sugestões**:
1. **Material didático oficial**
   - Guia para empresas: "Como avaliar se sou elegível à TSB?"
   - Guia para consultores: "Como certificar conformidade TSB?"
   - Vídeos explicativos por setor

2. **Certificação de consultores TSB**
   - Curso oficial sobre a taxonomia
   - Prova de certificação
   - Lista pública de consultores certificados

3. **Integração com ensino superior**
   - Disciplinas de finanças sustentáveis
   - TCC/dissertações usando dados TSB
   - Hackathons de soluções TSB

---

## 7. Impactos Esperados da TSB (Nossa Perspectiva)

### 7.1 Para Empresas

✅ **Oportunidades**:
- Acesso a financiamento verde (BNDES, bancos com linhas sustentáveis)
- Diferenciação competitiva (selo TSB)
- Transparência para investidores (ESG reporting)

⚠️ **Desafios**:
- Custo de compliance (auditoria, certificações)
- Complexidade técnica (especialmente PMEs)
- Risco de exclusão (critérios muito rígidos)

💡 **Nossa contribuição**:
- Ferramentas digitais de baixo custo para PMEs
- Auto-avaliação gratuita (tier básico)
- Consultoria acessível para adequação

### 7.2 Para Investidores

✅ **Oportunidades**:
- Critérios objetivos para portfólio verde
- Due diligence facilitada (TSB como checklist)
- Redução de risco de greenwashing

### 7.3 Para Políticas Públicas

✅ **Oportunidades**:
- Compras públicas sustentáveis (licitações exigindo TSB)
- Incentivos fiscais direcionados (ex: ICMS verde estadual)
- Monitoramento de NDC (metas climáticas)

💡 **Nossa contribuição**:
- Dashboard para gestores públicos (visualização setorial/regional)
- Integração com SINE (qualificação profissional direcionada)
- Relatórios para COP (mostrar progresso do Brasil)

### 7.4 Para Trabalhadores

✅ **Oportunidades**:
- Clareza sobre quais setores estão crescendo (empregos verdes)
- Sinalização para requalificação profissional
- Trabalho decente (Objetivo 8 da TSB)

💡 **Nossa contribuição**:
- Plataforma de matching com empresas TSB-conformes
- Trilhas de capacitação por setor TSB
- Transparência sobre salários e benefícios em setores verdes

---

## 8. Considerações Finais

A **Taxonomia Sustentável Brasileira** é um marco histórico para o país. Ela tem potencial de:

1. ✅ Mobilizar trilhões em investimento verde
2. ✅ Criar milhões de empregos sustentáveis
3. ✅ Posicionar o Brasil como líder em finanças sustentáveis
4. ✅ Garantir transição justa (objetivos sociais!)

Porém, para ser bem-sucedida, a TSB precisa ser:

- **Operacional**: Critérios claros e mensuráveis
- **Acessível**: Ferramentas digitais para empresas de todos os portes
- **Transparente**: Dados abertos e versionados
- **Evolutiva**: Revisões periódicas com participação ampla

A **Green Jobs Brasil** está pronta para contribuir tecnicamente em todas essas frentes. Oferecemos:

- 🔧 **Expertise técnica**: 3+ anos de experiência em classificação de empresas verdes
- 💻 **Infraestrutura digital**: Plataforma já operacional (API, dashboard, ETL)
- 🤝 **Espírito colaborativo**: Dados e código abertos para o bem comum
- 🎯 **Foco em impacto**: Nossa missão é acelerar a transição verde, não lucrar com greenwashing

**Estamos à disposição para reuniões técnicas, pilotos, ou qualquer forma de colaboração.**

---

**Contato**:  
Bruno Paixão  
Green Jobs Brasil  
Email: [contato]  
LinkedIn: [perfil]  
Site: [www.greenjobsbrasil.com.br]

**Agradecimentos**:  
Ao Ministério da Fazenda e todo o CITSB pela liderança nesta iniciativa essencial para o futuro sustentável do Brasil.

---

**Anexos**:
- [A1] Planilha de mapeamento CNAE → ODS (43 CNAEs atuais)
- [A2] Documentação técnica da API Green Jobs Brasil
- [A3] Exemplos de dashboard de conformidade
- [A4] Código-fonte dos scripts de ETL (GitHub)

**Versão**: 1.0  
**Data**: 12/11/2025
