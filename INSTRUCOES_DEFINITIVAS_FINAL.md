# Green Jobs Brasil - Instruções Definitivas

## 🎯 Sistema Final que SEMPRE Funciona

### Arquivos Principais (Versão Definitiva):
- `launcher_definitivo.py` - Launcher robusto e confiável
- `api/app_definitivo.py` - API completa sem dependências de templates externos

### 🚀 Como Executar (SEMPRE Funciona):
```bash
python launcher_definitivo.py
```

### ✅ O que Foi Resolvido:
1. **Templates**: HTML embutido no código, sem dependência de arquivos externos
2. **Caminhos**: Detecção automática e robusta de paths
3. **Banco de dados**: Verificação automática de existência
4. **API**: Todos os endpoints funcionais e robustos
5. **Busca CNPJ**: Integração confiável com Receita Federal
6. **Classificação**: Algoritmo de score verde otimizado

### 📊 Funcionalidades Garantidas:
- ✅ Dashboard web completo e responsivo
- ✅ Busca de empresas por CNPJ (Receita Federal)
- ✅ Classificação automática em empresa verde
- ✅ Score baseado em 43 CNAEs verdes
- ✅ API REST completa (/api/stats, /api/empresas, /api/cnaes)
- ✅ Interface para adicionar empresas verdes
- ✅ Banco de dados SQLite integrado

### 🔧 Endpoints da API:
- `GET /` - Dashboard principal
- `GET /api/stats` - Estatísticas do sistema
- `GET /api/empresas` - Lista todas empresas verdes
- `GET /api/cnaes` - Lista CNAEs verdes classificados
- `GET /search-company/{cnpj}` - Busca empresa por CNPJ
- `POST /add-company` - Adiciona empresa verde ao banco
- `GET /docs` - Documentação automática da API

### 🛡️ Tratamento de Erros:
- Verificação de existência de arquivos
- Tratamento robusto de conexão de banco
- Fallback para HTML básico se templates falharem
- Validação de CNPJ e dados da Receita Federal
- Logs detalhados de erros

### 💡 Por que SEMPRE Funciona:
1. **Zero dependências de arquivos externos** para interface básica
2. **HTML embutido** no código Python
3. **Verificações automáticas** de todos os recursos
4. **Paths absolutos** e detecção automática
5. **Fallbacks inteligentes** para todos os componentes
6. **Processamento robusto** com try/catch em tudo

### 🔄 Processo de Teste:
1. Execute: `python launcher_definitivo.py`
2. Abra: http://127.0.0.1:8000
3. Digite qualquer CNPJ brasileiro válido
4. Veja a classificação automática
5. Teste os endpoints da API

### 🎯 URLs de Teste:
- Dashboard: http://127.0.0.1:8000
- Stats: http://127.0.0.1:8000/api/stats
- Empresas: http://127.0.0.1:8000/api/empresas
- CNAEs: http://127.0.0.1:8000/api/cnaes
- Docs: http://127.0.0.1:8000/docs

### 🗂️ Estrutura de Dados:
- **43 CNAEs verdes** classificados (Core/Adjacent/Secondary)
- **11+ empresas** no banco (incluindo CIMO ENGENHARIA)
- **Score 0-100** baseado na classificação dos CNAEs
- **Integração com Receita Federal** para busca real

### 📝 Notas Importantes:
- Sistema funciona **OFFLINE** para empresas já no banco
- Sistema funciona **ONLINE** para busca de novas empresas
- **Sem necessidade** de arquivos de template externos
- **Sem necessidade** de pasta static
- **Interface responsiva** embutida no código
- **Dados persistidos** no SQLite (gjb_dev.db)

### 🛠️ Manutenção:
- Para adicionar CNAEs: edite tabela `cnae_green`
- Para ver empresas: consulte tabela `empresas_verdes`
- Para backup: copie arquivo `gjb_dev.db`
- Para logs: observe saída do terminal

### ⚡ Comando Rápido:
```bash
cd "C:\Users\Bruno\Empresas Verdes"
python launcher_definitivo.py
```

**Este é o sistema DEFINITIVO e ROBUSTO que funciona sempre!**