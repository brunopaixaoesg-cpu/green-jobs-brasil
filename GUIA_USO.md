# 🌱 Green Jobs Brasil - Guia de Uso

## 🚀 3 Formas de Usar o Sistema

### 1. 🖱️ Interface Gráfica (Mais Fácil)
```bash
# Execute o launcher
python launcher.py
```
- Clique em "🚀 Iniciar Sistema"
- Use os botões para acessar funcionalidades
- Interface amigável com log em tempo real

### 2. 🖥️ Arquivo Batch (Windows)
```bash
# Execute o arquivo batch
iniciar_green_jobs.bat
```
- Duplo clique no arquivo
- Sistema inicia automaticamente
- Interface de terminal colorida

### 3. ⌨️ Linha de Comando (Avançado)
```bash
# Vá para o diretório
cd "C:\Users\Bruno\Empresas Verdes"

# Inicie a API
python start_api.py
```

## 📋 O que Fazer Após Iniciar

### 1. Acesse a Documentação
- **URL**: http://127.0.0.1:8000/docs
- **O que é**: Interface interativa para testar a API
- **Como usar**: Clique nos endpoints para testar

### 2. Consulte Empresas Verdes
- **URL**: http://127.0.0.1:8000/empresas
- **Filtros disponíveis**:
  - `?uf=SP` - Filtrar por estado
  - `?q=solar` - Buscar por palavra-chave
  - `?limit=20` - Limitar resultados

### 3. Explore CNAEs Verdes
- **URL**: http://127.0.0.1:8000/cnaes
- **Filtros disponíveis**:
  - `?categoria=Energia` - Por categoria
  - `?prioridade=Core` - Por prioridade

### 4. Veja Estatísticas
- **URL**: http://127.0.0.1:8000/stats
- **Dados**: Total empresas, CNAEs, distribuição por UF

## 🔧 Exemplos Práticos de Uso

### Para Pesquisadores
```bash
# Empresas de energia solar em São Paulo
http://127.0.0.1:8000/empresas?uf=SP&q=solar

# CNAEs de economia circular
http://127.0.0.1:8000/cnaes?categoria=Economia+Circular

# Estatísticas completas
http://127.0.0.1:8000/stats
```

### Para Desenvolvedores
```python
import requests

# Buscar empresas verdes
response = requests.get('http://127.0.0.1:8000/empresas')
empresas = response.json()

# Filtrar por UF
response = requests.get('http://127.0.0.1:8000/empresas?uf=RJ')
empresas_rj = response.json()

# Obter detalhes de empresa específica
cnpj = "12345678000195"
response = requests.get(f'http://127.0.0.1:8000/empresas/{cnpj}')
empresa = response.json()
```

### Para Analistas de Dados
```bash
# Exportar dados via API e processar
curl "http://127.0.0.1:8000/empresas?limit=1000" > empresas.json
curl "http://127.0.0.1:8000/cnaes" > cnaes.json
curl "http://127.0.0.1:8000/stats" > estatisticas.json
```

## 📊 Dados Disponíveis Atualmente

### Empresas (10 registros exemplo)
- CNPJ, Razão Social, Nome Fantasia
- CNAE Principal, CNAEs Secundários
- UF, Município, Porte
- Score Verde (0-100)
- Status, Data de Abertura

### CNAEs Verdes (43 classificados)
- Código CNAE, Título, Categoria
- Prioridade (Core/Adjacent/Secondary)
- Objetivos de Desenvolvimento Sustentável (ODS)
- Observações

### Relacionamentos (17 vínculos)
- Empresa ↔ CNAE
- Principal + Secundários

## 🎯 Casos de Uso Reais

### 1. 🏦 Instituições Financeiras
**Objetivo**: Identificar empresas para crédito verde
```bash
# Empresas com alto score verde
http://127.0.0.1:8000/empresas?limit=50
# Filtrar por score_verde >= 70
```

### 2. 🏛️ Governo/Órgãos Públicos
**Objetivo**: Mapear economia verde por região
```bash
# Estatísticas por UF
http://127.0.0.1:8000/stats
# Empresas por categoria sustentável
```

### 3. 💼 Investidores ESG
**Objetivo**: Encontrar oportunidades de investimento
```bash
# CNAEs de maior prioridade
http://127.0.0.1:8000/cnaes?prioridade=Core
# Empresas em setores emergentes
```

### 4. 🎓 Pesquisadores
**Objetivo**: Estudar transição energética
```bash
# Empresas de energia renovável
http://127.0.0.1:8000/empresas?q=energia
# CNAEs relacionados ao ODS 7
```

## 🔄 Próximos Passos

### Curto Prazo (1-2 semanas)
1. **Testar intensivamente** o sistema atual
2. **Coletar feedback** de usuários iniciais
3. **Documentar bugs** e melhorias necessárias
4. **Preparar dados reais** da Receita Federal

### Médio Prazo (1-3 meses)
1. **Processar dados completos** da RFB (milhões de empresas)
2. **Desenvolver interface web** amigável
3. **Adicionar filtros avançados** (geolocalização, porte, setor)
4. **Implementar APIs de terceiros** (mapas, dados financeiros)

### Longo Prazo (3-6 meses)
1. **Deploy em produção** (AWS/Azure)
2. **Sistema de usuários** e autenticação
3. **Dashboards interativos** com visualizações
4. **Parcerias comerciais** e monetização

## 📞 Suporte e Contato

### Problemas Técnicos
1. Verifique se Python está instalado
2. Confirme que todas as dependências estão instaladas
3. Execute `python check_db.py` para validar dados
4. Verifique logs em `launcher.py` ou terminal

### Melhorias e Sugestões
- Documente casos de uso específicos
- Sugira novos CNAEs para classificação
- Proponha funcionalidades prioritárias
- Compartilhe feedback de uso real

---

**Green Jobs Brasil** - Transformando dados em oportunidades verdes! 🌱🇧🇷