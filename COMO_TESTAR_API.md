# 🚀 COMO TESTAR A API LOCALMENTE

## Método 1: Script Python (start_api.py) ✅ ATUALIZADO

### Passo 1: Iniciar API

```bash
# No terminal PowerShell
cd "C:\Users\Bruno\Empresas Verdes"
C:/Users/Bruno/AppData/Local/Programs/Python/Python313/python.exe start_api.py
```

**Você verá**:
```
🚀 Iniciando Green Jobs Brasil API...
📍 API: http://127.0.0.1:8002
📚 Docs: http://127.0.0.1:8002/docs
🔍 TSB: http://127.0.0.1:8002/api/taxonomia/objetivos
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8002
...
✅ Router taxonomia TSB registrado
INFO:     Application startup complete.
```

### Passo 2: Testar no navegador

Abra no seu navegador:
- **Documentação**: http://127.0.0.1:8002/docs
- **Health**: http://127.0.0.1:8002/health
- **TSB Objetivos**: http://127.0.0.1:8002/api/taxonomia/objetivos

---

## Método 2: Script Batch Automatizado

### Passo 1: Iniciar API
```bash
# Clique duplo ou execute no PowerShell:
start_api.py
```

### Passo 2: Testar (em OUTRO terminal)
```bash
# Clique duplo em:
TESTAR_API.bat
```

**Resultado esperado**:
```
🧪 TESTANDO API - GREEN JOBS BRASIL
============================================================
📋 TESTANDO ENDPOINTS BÁSICOS
✅ Health check OK

🌱 TESTANDO TSB - OBJETIVOS
✅ TSB Objetivos OK (11 objetivos)

🏢 TESTANDO TSB - SETORES  
✅ TSB Setores OK (8 setores)

📊 TESTANDO EMPRESAS COM TSB
✅ Empresas com TSB OK

============================================================
✅ TODOS OS TESTES CONCLUÍDOS!
```

---

## Método 3: Comandos Curl Manuais

Com a API rodando, teste manualmente:

### Health Check
```bash
curl http://127.0.0.1:8002/health
```

### TSB - Todos os Objetivos
```bash
curl http://127.0.0.1:8002/api/taxonomia/objetivos
```

### TSB - Objetivo Específico
```bash
curl http://127.0.0.1:8002/api/taxonomia/objetivos/1
```

### TSB - Setores
```bash
curl http://127.0.0.1:8002/api/taxonomia/setores
```

### TSB - Info
```bash
curl http://127.0.0.1:8002/api/taxonomia/
```

### Empresas (Paginado)
```bash
curl http://127.0.0.1:8002/empresas/api/listar
```

### Empresas COM TSB (enriquecidas)
```bash
curl "http://127.0.0.1:8002/empresas/api/listar?tsb=true&limit=5"
```

---

## Método 4: Script Python de Teste

```bash
# Execute em OUTRO terminal (com API rodando):
C:/Users/Bruno/AppData/Local/Programs/Python/Python313/python.exe test_api.py
```

**Resultado**:
```
🧪 TESTE RÁPIDO - GREEN JOBS BRASIL API
============================================================

📋 ENDPOINTS BÁSICOS
------------------------------------------------------------
✅ Health Check: OK (200)
✅ Documentação Swagger: OK (200)
✅ Stats Gerais: OK (200)

🌱 ENDPOINTS TSB
------------------------------------------------------------
✅ TSB Objetivos: OK (200)
   → 11 objetivos carregados
✅ TSB Setores: OK (200)
   → 8 setores carregados
✅ TSB Critérios: OK (200)
✅ TSB Info: OK (200)

🏢 ENDPOINTS EMPRESAS
------------------------------------------------------------
✅ Listar Empresas: OK (200)
✅ Empresas com TSB: OK (200)
   → Enriquecimento TSB: ✅
   → TSB Elegível: True
   → TSB Score: 100.0

============================================================
📊 RESULTADO: 10/10 testes passaram
============================================================
✅ TODOS OS TESTES PASSARAM!
```

---

## ⚠️ Troubleshooting

### Erro: "Python não encontrado"
**Solução**: Use o caminho completo:
```bash
C:/Users/Bruno/AppData/Local/Programs/Python/Python313/python.exe start_api.py
```

### Erro: "Address already in use"
**Solução**: Matar processo na porta 8002:
```bash
# PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8002).OwningProcess | Stop-Process
```

### Erro: "Connection refused"
**Solução**: Certifique-se que a API está rodando:
```bash
# Verifique se apareceu: "Application startup complete."
```

### API não recarrega automaticamente
**Solução**: É normal! O `--reload` está ativo, salve arquivos para recarregar.

---

## 🎯 Checklist de Funcionamento

Quando a API inicia corretamente, você vê:

- [x] `✅ Health router carregado com sucesso!`
- [x] `✅ Profissionais router carregado com sucesso!`
- [x] `✅ Empresas router carregado com sucesso!`
- [x] `✅ KPIs router carregado com sucesso!`
- [x] `✅ Vagas router carregado com sucesso!`
- [x] `✓ Router auth registrado`
- [x] `✓ Router health registrado`
- [x] `✓ Router taxonomia TSB registrado` ← **IMPORTANTE!**
- [x] `INFO: Application startup complete.`

---

## 📚 Documentação Interativa

Acesse: **http://127.0.0.1:8002/docs**

Lá você pode:
- ✅ Ver TODOS os endpoints disponíveis
- ✅ Testar cada endpoint direto no navegador
- ✅ Ver schemas de request/response
- ✅ Fazer autenticação se necessário
- ✅ Explorar endpoints TSB interativamente

---

## 🎉 Tudo Funcionando?

Se todos os testes passaram:

### Próximos Passos:

1. ✅ **Explorar Swagger**: http://127.0.0.1:8002/docs
2. ✅ **Testar TSB Info**: http://127.0.0.1:8002/api/taxonomia/info
3. ✅ **Ver Objetivos**: http://127.0.0.1:8002/api/taxonomia/objetivos
4. ✅ **Empresas TSB**: http://127.0.0.1:8002/api/empresas?tsb=true

### Para Deploy:

Quando pronto para produção:
1. Leia: `DEPLOY_RENDER.md`
2. Faça push para GitHub (já feito! ✅)
3. Conecte Render.com
4. Deploy automático! 🚀

---

**Data**: 14/11/2025  
**Versão API**: 1.6.0  
**Status**: ✅ Funcionando localmente com TSB!
