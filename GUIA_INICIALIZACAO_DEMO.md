# 🚀 GUIA DE INICIALIZAÇÃO - GREEN JOBS BRASIL
## Sistema Completo de Vagas ESG

### 📋 PRÉ-REQUISITOS
- ✅ Python 3.13+ instalado
- ✅ Conexão com internet (para validação CNPJ)
- ✅ Navegador web moderno

### 🎯 INICIALIZAÇÃO RÁPIDA (3 PASSOS)

#### 1️⃣ Abrir Terminal/PowerShell
```powershell
cd "C:\Users\Bruno\Empresas Verdes"
```

#### 2️⃣ Iniciar Sistema
```powershell
python start_api.py
```
**Aguarde ver as mensagens:**
```
✅ Banco de dados inicializado!
INFO: Application startup complete.
```

#### 3️⃣ Abrir Navegador
- **API Principal**: http://127.0.0.1:8002
- **Documentação**: http://127.0.0.1:8002/docs

---

## 🌐 PÁGINAS PRINCIPAIS PARA DEMONSTRAÇÃO

### 👥 PARA CANDIDATOS
| Página | URL | Descrição |
|--------|-----|-----------|
| **Lista de Vagas** | http://127.0.0.1:8002/vagas | 6 vagas ESG disponíveis |
| **Candidatar-se** | Clicar "Candidatar-se" | Modal com formulário completo |

### 🏢 PARA EMPRESAS  
| Página | URL | Descrição |
|--------|-----|-----------|
| **Dashboard** | http://127.0.0.1:8002/dashboard_empresa/1 | Painel empresa Green Tech |
| **Criar Vaga** | http://127.0.0.1:8002/criar_vaga | Formulário nova vaga |
| **Cadastro** | http://127.0.0.1:8002/cadastro_empresa | Registro nova empresa |

### 🧪 TESTE COMPLETO
| Página | URL | Descrição |
|--------|-----|-----------|
| **Teste Sistema** | http://127.0.0.1:8002/teste_sistema | Validação completa |

---

## 📊 DADOS PRÉ-CARREGADOS

### 🌱 PROFISSIONAIS (120 cadastrados)
- **34** Engenheiros Ambientais
- **32** Engenheiros Florestais  
- **29** Consultores Ambientais
- **20** Analistas ESG
- **5** Biólogos Ambientais

**Habilidades incluídas:**
- Geoprocessamento (QGIS, ArcGIS, Google Earth Engine)
- Inventários Florestais e Manejo
- Licenciamento e Compliance Ambiental
- Relatórios ESG (GRI, SASB, TCFD)

### 🏢 EMPRESAS (2 ativas)
1. **Green Tech Solutions** (Score ESG: 95%)
   - CNPJ: 60.331.021/0001-11
   - 3 vagas ativas
   
2. **EcoConsult Ambiental** (Score ESG: 88%)
   - CNPJ: 12.345.678/0001-90
   - 3 vagas ativas

### 💼 VAGAS (6 disponíveis)
1. **Analista de Sustentabilidade Jr** - R$ 4.000-6.000 (SP)
2. **Coordenador de ESG** - R$ 7.000-10.000 (SP, Remoto)
3. **Especialista em GIS** - R$ 8.000-12.000 (Campinas)
4. **Biólogo Ambiental** - R$ 6.000-8.500 (RJ)
5. **Engenheiro Florestal** - R$ 9.000-13.000 (BH)
6. **Consultor Ambiental** - R$ 12.000-18.000 (SP, Remoto)

---

## 🎭 ROTEIRO DE DEMONSTRAÇÃO

### 🎬 CENÁRIO 1: CANDIDATO PROCURA VAGA (3 min)
1. Acessar http://127.0.0.1:8002/vagas
2. Mostrar **6 vagas ESG** com filtros
3. Clicar "**Candidatar-se**" em uma vaga
4. Preencher formulário:
   - Nome: Bruno Paixão
   - Email: bruno.paixao.esg@gmail.com
   - Experiência ESG: 5 anos
   - Habilidades: Relatórios de Sustentabilidade, GRI
5. Enviar e mostrar **score de compatibilidade**

### 🎬 CENÁRIO 2: EMPRESA VÊ CANDIDATURAS (2 min)
1. Acessar http://127.0.0.1:8002/dashboard_empresa/1
2. Mostrar dados da **Green Tech Solutions**
3. Ver **vagas criadas** e **candidaturas recebidas**
4. Mostrar **estatísticas** em tempo real

### 🎬 CENÁRIO 3: CRIAR NOVA VAGA (3 min)
1. Acessar http://127.0.0.1:8002/criar_vaga
2. Preencher formulário completo:
   - Título: Especialista em Carbono
   - Localização: São Paulo, SP
   - Salário: R$ 8.000-12.000
   - Nível: Sênior
3. Salvar e mostrar na lista

### 🎬 CENÁRIO 4: CADASTRO EMPRESA (3 min)
1. Acessar http://127.0.0.1:8002/cadastro_empresa
2. Mostrar **4 etapas** do cadastro
3. Testar **validação CNPJ** em tempo real
4. Mostrar **cálculo score ESG automático**

---

## 🔧 COMANDOS ÚTEIS

### Parar Sistema
```powershell
Ctrl + C
```

### Verificar Status
```powershell
curl http://127.0.0.1:8002/api/vagas
```

### Verificar Banco
```powershell
python verificar_banco_completo.py
```

### Repopular Dados
```powershell
python popular_profissionais_completo.py
```

---

## 🎯 PONTOS FORTES PARA DESTACAR

### ✨ DIFERENCIAIS TÉCNICOS
- ✅ **Validação CNPJ em tempo real** (API ReceitaWS)
- ✅ **Score ESG automático** (0-100 baseado em ODS)
- ✅ **Sistema de compatibilidade** (candidato x vaga)
- ✅ **Interface responsiva** (mobile-first)
- ✅ **API REST completa** (6+ endpoints)

### 🌱 FOCO AMBIENTAL
- ✅ **120 profissionais** especializados em ESG
- ✅ **Áreas específicas**: Biologia, Eng. Florestal, Eng. Ambiental
- ✅ **Habilidades técnicas**: QGIS, ArcGIS, GEE, inventários
- ✅ **Consultoria especializada** em licenciamento

### 📈 ESCALABILIDADE
- ✅ **Banco SQLite** (fácil deploy)
- ✅ **FastAPI** (alta performance)
- ✅ **Modular** (fácil expansão)
- ✅ **Docker ready** (deploy containerizado)

---

## ⚠️ TROUBLESHOOTING

### Erro "conexão recusada"
```powershell
taskkill /f /im python.exe
python start_api.py
```

### Banco vazio
```powershell
python popular_profissionais_completo.py
```

### Port em uso
```powershell
netstat -ano | findstr :8002
taskkill /f /pid [PID_NUMBER]
```

---

## 🎉 SISTEMA PRONTO!

O **Green Jobs Brasil** está 100% funcional e pronto para:
- 🎭 **Demonstrações comerciais**
- 👥 **Testes de usuário** 
- 🚀 **Deploy em produção**
- 📊 **Análise de métricas**

**Status: OPERACIONAL** ✅