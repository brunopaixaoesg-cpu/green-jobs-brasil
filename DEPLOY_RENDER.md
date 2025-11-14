# 🚀 GUIA DE DEPLOY - RENDER.COM

## Green Jobs Brasil API - Deploy em Produção

Este guia detalha o processo completo de deploy da API Green Jobs Brasil no Render.com.

---

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Código comitado e pushed para GitHub
- ✅ Conta no Render.com (gratuita)
- ✅ Arquivos de deploy no repositório:
  - `render.yaml`
  - `build.sh`
  - `requirements.txt`

---

## 🎯 PASSO 1: Preparar Repositório GitHub

### 1.1. Verificar arquivos

```bash
# Verificar se os arquivos estão presentes
ls -la | grep -E "render.yaml|build.sh|requirements.txt"

# Deve mostrar:
# -rw-r--r--  render.yaml
# -rwxr-xr-x  build.sh
# -rw-r--r--  requirements.txt
```

### 1.2. Commit e Push

```bash
# Adicionar arquivos de deploy
git add render.yaml build.sh requirements.txt

# Commit
git commit -m "feat(deploy): configuração para Render.com

- render.yaml com web service + PostgreSQL
- build.sh com setup automatizado
- requirements.txt com versões específicas
- settings.py com suporte DATABASE_URL"

# Push para main (ou branch principal)
git push origin main
```

### 1.3. Verificar no GitHub

Acesse: `https://github.com/brunopaixaoesg-cpu/green-jobs-brasil`

Confirme que os arquivos estão lá.

---

## 🌐 PASSO 2: Criar Conta no Render

### 2.1. Acessar Render.com

1. Vá para: https://render.com
2. Clique em **"Get Started"** ou **"Sign Up"**
3. Escolha: **"Sign up with GitHub"**
4. Autorize o Render a acessar seus repositórios

### 2.2. Conectar Repositório

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Blueprint"**
3. Procure por: `green-jobs-brasil`
4. Clique em **"Connect"**

O Render irá:
- ✅ Detectar o `render.yaml` automaticamente
- ✅ Criar o PostgreSQL database primeiro
- ✅ Criar o web service depois
- ✅ Configurar todas as env vars

---

## 🗄️ PASSO 3: Configurar Database

O Render criará automaticamente baseado no `render.yaml`:

```yaml
databases:
  - name: greenjobs-db
    plan: free
    databaseName: greenjobs
    user: greenjobs_user
```

### 3.1. Verificar Database

1. No dashboard, vá para **"Databases"**
2. Clique em `greenjobs-db`
3. Anote as informações:
   - **Host**: oregon-postgres.render.com
   - **Database**: greenjobs
   - **User**: greenjobs_user
   - **Internal URL**: postgresql://greenjobs_user:...

### 3.2. Connection String

O Render injeta automaticamente em `DATABASE_URL`:

```
postgresql://greenjobs_user:PASSWORD@HOST/greenjobs
```

---

## 🚀 PASSO 4: Deploy do Web Service

### 4.1. Primeira Build

O Render automaticamente:

1. ✅ Clona o repositório
2. ✅ Executa `bash build.sh`:
   - Atualiza pip
   - Instala requirements.txt
   - Cria diretórios (logs, uploads)
   - Testa importação de settings
3. ✅ Inicia: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### 4.2. Acompanhar Logs

No dashboard:
- Clique em `greenjobs-api`
- Vá para aba **"Logs"**
- Veja o progresso em tempo real

### 4.3. Build Esperado (sucesso)

```
🚀 Starting Green Jobs Brasil build...
📦 Upgrading pip...
📦 Installing dependencies...
📁 Creating necessary directories...
✅ DATABASE_URL found
🧪 Running smoke test...
✅ Settings loaded: Green Jobs Brasil
✅ Environment: production
✅ TSB Enabled: True
✅ Build completed successfully!
```

---

## 🔧 PASSO 5: Configurar Variáveis Adicionais

Embora o `render.yaml` configure a maioria, você pode adicionar manualmente:

### 5.1. Acessar Environment

1. Dashboard → `greenjobs-api`
2. Aba **"Environment"**
3. Clique em **"Add Environment Variable"**

### 5.2. Variáveis Críticas

**SECRET_KEY** (se não auto-gerado):
```bash
# Gerar localmente
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar resultado e adicionar no Render
```

**BASE_URL**:
```
https://greenjobs-api.onrender.com
```

**CORS_ORIGINS** (após deploy frontend):
```
https://greenjobs-web.onrender.com,https://greenjobs.com.br
```

### 5.3. Salvar e Redeploy

Após adicionar variáveis:
- Clique em **"Save Changes"**
- Render fará redeploy automático

---

## ✅ PASSO 6: Validar Deploy

### 6.1. URL da API

A API estará disponível em:
```
https://greenjobs-api.onrender.com
```

### 6.2. Health Check

Teste o endpoint de saúde:

```bash
curl https://greenjobs-api.onrender.com/health

# Resposta esperada:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-14T...",
  "version": "1.6.0",
  "features": {
    "tsb": true,
    "ml_matching": true,
    "storytelling": true
  }
}
```

### 6.3. Documentação Swagger

Acesse:
```
https://greenjobs-api.onrender.com/docs
```

Você deve ver:
- ✅ Todos os endpoints TSB
- ✅ Autenticação
- ✅ Empresas, Profissionais, Vagas
- ✅ Documentação interativa

### 6.4. Testar Endpoints TSB

```bash
# Objetivos TSB
curl https://greenjobs-api.onrender.com/api/taxonomia/objetivos

# Setores
curl https://greenjobs-api.onrender.com/api/taxonomia/setores

# Info
curl https://greenjobs-api.onrender.com/api/taxonomia/info
```

---

## 📊 PASSO 7: Monitoramento

### 7.1. Dashboard Render

No dashboard você pode ver:
- **CPU Usage**: Uso de processador
- **Memory**: Consumo de memória
- **Response Time**: Latência das requisições
- **Error Rate**: Taxa de erros

### 7.2. Logs

Acesse logs em tempo real:
```
Dashboard → greenjobs-api → Logs
```

Formato JSON facilita parsing:
```json
{
  "timestamp": "2025-11-14T12:00:00",
  "level": "INFO",
  "message": "API iniciada",
  "tsb": true
}
```

### 7.3. Alertas

Configure alertas (plano pago):
- Deploy failures
- High error rate
- Performance degradation

---

## 🔄 PASSO 8: Deploys Futuros

### 8.1. Auto-Deploy

Com `autoDeploy: true` no `render.yaml`:

```bash
# Qualquer push para main faz redeploy automático
git add .
git commit -m "feat: nova funcionalidade"
git push origin main

# Render detecta e faz deploy automaticamente
```

### 8.2. Deploy Manual

No dashboard:
1. `greenjobs-api` → **"Manual Deploy"**
2. Escolha branch
3. Clique em **"Deploy"**

### 8.3. Rollback

Se algo der errado:
1. `greenjobs-api` → **"Events"**
2. Encontre deploy anterior estável
3. Clique em **"Redeploy"**

---

## 🐛 TROUBLESHOOTING

### Build Falha

**Erro**: `ModuleNotFoundError`
```bash
# Solução: Adicionar módulo ao requirements.txt
pip freeze | grep nome-do-modulo
# Adicionar ao requirements.txt
git commit -am "fix: adicionar dependência X"
git push
```

**Erro**: `Permission denied: build.sh`
```bash
# Solução: Dar permissão de execução
chmod +x build.sh
git add build.sh
git commit -m "fix: permissão build.sh"
git push
```

### Database Connection Error

**Erro**: `could not connect to server`

Soluções:
1. Verificar se database está "Available" no dashboard
2. Verificar DATABASE_URL está configurado
3. Checar internal database URL no Render

### Application Crash

**Erro**: `Application failed to start`

Debug:
1. Ver logs completos no dashboard
2. Verificar health check path: `/health`
3. Testar localmente com mesmas env vars

### Free Tier Sleep

⚠️ **Importante**: Free tier hiberna após 15min inatividade

Soluções:
- **UptimeRobot**: Ping a cada 5min (gratuito)
- **Upgrade para Starter**: $7/mês, sem hibernação

---

## 💰 CUSTOS

### Free Tier (Atual)

- ✅ **Web Service**: Free
  - 512 MB RAM
  - Shared CPU
  - Hiberna após 15min
  - 750 horas/mês

- ✅ **Database**: Free
  - 256 MB storage
  - PostgreSQL
  - Backups automáticos

**Total**: $0/mês

### Starter (Produção Real)

- **Web Service**: $7/mês
  - 512 MB RAM
  - Shared CPU
  - **SEM hibernação**
  - 24/7 disponível

- **Database**: $7/mês
  - 1 GB storage
  - PostgreSQL
  - Backups diários

**Total**: $14/mês

---

## 🔐 SEGURANÇA

### SSL/TLS

✅ **Automático**: Render fornece SSL grátis para todos os serviços

Sua API já está em:
```
https://greenjobs-api.onrender.com
```

### Secrets

- SECRET_KEY: Auto-gerado pelo Render
- Database password: Auto-gerado
- Nunca comitar secrets no código

### CORS

Configurar apenas origins necessários:

```yaml
# render.yaml
- key: CORS_ORIGINS
  value: https://greenjobs-web.onrender.com,https://greenjobs.com.br
```

---

## 📱 DOMÍNIO CUSTOMIZADO

### Configurar Domínio

Se você tem `greenjobs.com.br`:

1. Dashboard → `greenjobs-api` → **"Settings"**
2. **"Custom Domain"** → **"Add Custom Domain"**
3. Digite: `api.greenjobs.com.br`
4. Configurar DNS:

```
Type: CNAME
Name: api
Value: greenjobs-api.onrender.com
```

5. Aguardar propagação DNS (até 48h)
6. SSL automático após verificação

---

## 🎯 CHECKLIST DE DEPLOY

- [ ] Código pushed para GitHub (branch main)
- [ ] Conta Render criada e conectada ao GitHub
- [ ] Blueprint detectou `render.yaml`
- [ ] Database criado e disponível
- [ ] Web service deployado com sucesso
- [ ] Health check retorna `200 OK`
- [ ] Swagger docs acessível
- [ ] Endpoints TSB funcionando
- [ ] Logs sem erros críticos
- [ ] SECRET_KEY configurado
- [ ] CORS configurado para domínios corretos
- [ ] Monitoramento ativo

---

## 📞 SUPORTE

### Render Support

- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Green Jobs Brasil

- Repo: https://github.com/brunopaixaoesg-cpu/green-jobs-brasil
- Issues: Criar issue no GitHub
- Docs: Ver `/docs` na API

---

## 🎉 PRÓXIMOS PASSOS

Após deploy bem-sucedido:

1. ✅ **Testar API em produção**
   - Criar usuários teste
   - Importar empresas
   - Testar matching

2. ✅ **Configurar Frontend**
   - Deploy frontend no Render
   - Conectar com API de produção
   - Testar fluxo completo

3. ✅ **Monitoramento**
   - Configurar UptimeRobot
   - Integrar Sentry (erros)
   - Configurar Analytics

4. ✅ **Documentação**
   - API Reference completa
   - Postman Collection
   - Exemplos de integração

---

**Data de Criação**: 14/11/2025  
**Versão**: 1.0  
**Autor**: Green Jobs Brasil Team  
**Status**: ✅ Pronto para uso
