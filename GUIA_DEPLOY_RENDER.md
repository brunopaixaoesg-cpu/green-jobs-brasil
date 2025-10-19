# 🚀 Deploy Green Jobs Brasil - Render.com (GRÁTIS)

## 📋 O que você vai conseguir

Após seguir este guia, você terá:
- ✅ URL pública: `https://greenjobs-brasil.onrender.com`
- ✅ SSL/HTTPS automático
- ✅ Acessível de qualquer lugar (celular, desktop)
- ✅ 100% grátis para hobby projects
- ✅ Deploy automático via GitHub

---

## 🎯 Passo a Passo Completo

### Passo 1: Preparar Arquivos

#### 1.1 Criar `requirements.txt` na raiz do projeto

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
pydantic==2.5.0
passlib==1.7.4
python-jose[cryptography]==3.3.0
bcrypt==4.1.1
```

#### 1.2 Criar `render.yaml` na raiz (opcional, mas recomendado)

```yaml
services:
  - type: web
    name: greenjobs-brasil
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn api.sqlite_api_clean:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
```

#### 1.3 Modificar `api/sqlite_api_clean.py`

**No final do arquivo, trocar:**

```python
if __name__ == "__main__":
    print("=" * 50)
    print("API: http://127.0.0.1:8002")
    print("Docs: http://127.0.0.1:8002/docs")
    print("ML: Sistema de Matching Inteligente Ativo")
    print("Foco: Profissionais e Vagas Ambientais")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8002)
```

**Por:**

```python
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8002))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print("=" * 50)
    print(f"API: http://{host}:{port}")
    print(f"Docs: http://{host}:{port}/docs")
    print("ML: Sistema de Matching Inteligente Ativo")
    print("Foco: Profissionais e Vagas Ambientais")
    print("=" * 50)
    
    uvicorn.run(app, host=host, port=port)
```

---

### Passo 2: Criar Repositório no GitHub

#### 2.1 Inicializar Git (se ainda não fez)

```bash
cd "C:\Users\Bruno\Empresas Verdes"
git init
```

#### 2.2 Criar `.gitignore`

```txt
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.db-journal
.env
.vscode/
.idea/
*.log
```

#### 2.3 Criar repositório no GitHub

1. Acesse https://github.com/new
2. Nome: `green-jobs-brasil`
3. Público ou Privado (sua escolha)
4. Não inicialize com README (já tem local)
5. Criar repositório

#### 2.4 Fazer primeiro commit

```bash
git add .
git commit -m "Initial commit - Green Jobs Brasil v1.0"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/green-jobs-brasil.git
git push -u origin main
```

---

### Passo 3: Deploy no Render.com

#### 3.1 Criar Conta

1. Acesse https://render.com
2. "Get Started for Free"
3. Login com GitHub (recomendado)

#### 3.2 Criar Web Service

1. Dashboard → "New +" → "Web Service"
2. Conectar repositório GitHub
3. Selecionar `green-jobs-brasil`
4. Configurar:

**Configurações:**
- **Name**: `greenjobs-brasil`
- **Region**: `Oregon (US West)` ou mais próximo
- **Branch**: `main`
- **Root Directory**: (deixar vazio)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api.sqlite_api_clean:app --host 0.0.0.0 --port $PORT`

**Plano:**
- **Instance Type**: `Free` (0$/month)

5. Clicar em "Create Web Service"

#### 3.3 Aguardar Deploy

- ⏳ Render vai instalar dependências (2-3 minutos)
- ⏳ Build e deploy (1-2 minutos)
- ✅ Status: "Live" → Pronto!

#### 3.4 Acessar Aplicação

**URL gerada:**
```
https://greenjobs-brasil.onrender.com
```

**Testar:**
- Dashboard: `https://greenjobs-brasil.onrender.com/api/profissionais/dashboard/1`
- API Docs: `https://greenjobs-brasil.onrender.com/docs`

---

## ⚙️ Configurações Avançadas (Opcional)

### Variáveis de Ambiente

No painel do Render:
1. Ir em "Environment"
2. Adicionar variáveis:

```
SECRET_KEY=sua-chave-super-secreta-aqui
DATABASE_URL=sqlite:///./gjb_dev.db
ENVIRONMENT=production
```

### Custom Domain

1. Registrar domínio (ex: Registro.br, Namecheap)
2. No Render: Settings → Custom Domain
3. Adicionar domínio: `greenjobs.com.br`
4. Configurar DNS:
   - CNAME: `@` → `greenjobs-brasil.onrender.com`
   - CNAME: `www` → `greenjobs-brasil.onrender.com`

---

## 🔧 Troubleshooting

### Problema: App não inicia

**Solução 1**: Verificar logs
- Render Dashboard → Logs
- Procurar por erros de import ou dependências

**Solução 2**: Verificar requirements.txt
```bash
pip freeze > requirements.txt
```

### Problema: Erro 502 Bad Gateway

**Causa**: App não está escutando na porta correta

**Solução**: Garantir que `$PORT` está sendo usado
```python
port = int(os.environ.get("PORT", 8002))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Problema: App "dorme" após 15 minutos

**Causa**: Free tier do Render tem sleep automático

**Soluções**:
1. **Aceitar** (primeira requisição demora ~30s para acordar)
2. **UptimeRobot** (ping a cada 5 min) - `https://uptimerobot.com`
3. **Upgrade** para plano pago ($7/mês) - sem sleep

### Problema: Banco de dados não persiste

**Causa**: SQLite em disco efêmero (Render deleta após redeploy)

**Solução**: Migrar para PostgreSQL
```bash
# No Render Dashboard
New → PostgreSQL
# Copiar DATABASE_URL
# Modificar código para usar PostgreSQL
```

---

## 📊 Monitoramento

### UptimeRobot (Grátis)

1. Criar conta: https://uptimerobot.com
2. Add New Monitor:
   - Type: HTTP(s)
   - URL: `https://greenjobs-brasil.onrender.com`
   - Interval: 5 minutes
3. Receber alertas por email se cair

### Analytics (Opcional)

Adicionar Google Analytics ou Plausible no HTML:

```html
<!-- No <head> de todas as páginas -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🎯 Próximos Passos

Após deploy no Render:

1. ✅ Testar no celular
2. ✅ Compartilhar link com primeiros usuários
3. ✅ Coletar feedback
4. ✅ Adicionar domínio personalizado
5. ✅ Migrar para PostgreSQL (se escalar)
6. ✅ Configurar CI/CD (GitHub Actions)

---

## 💰 Custos Estimados

### Fase MVP (Free Forever)
- **Render Free Tier**: $0/mês
- **GitHub**: $0/mês
- **Total**: **$0/mês** ✅

### Fase Piloto (Primeiros Clientes)
- **Render Starter**: $7/mês (sem sleep)
- **PostgreSQL**: $7/mês (25GB)
- **Domínio .br**: R$40/ano (~R$3/mês)
- **Total**: **~$17/mês**

### Fase Produção (Escalando)
- **VPS DigitalOcean**: $12/mês (2GB RAM)
- **PostgreSQL Managed**: $15/mês
- **Domínio + SSL**: R$3/mês
- **CDN Cloudflare**: $0/mês (free tier)
- **Total**: **~$30/mês**

---

## ✅ Checklist Final

Antes de considerar "online":

- [ ] Deploy no Render funcionando
- [ ] URL pública acessível
- [ ] Testado no celular
- [ ] API Docs acessível
- [ ] Todas as rotas funcionando
- [ ] SECRET_KEY mudada
- [ ] CORS configurado
- [ ] Logs monitorados
- [ ] Backup do banco (mesmo SQLite)
- [ ] Domínio customizado (opcional)

---

**Pronto para fazer o deploy?**

Posso ajudar com:
1. Criar os arquivos necessários (requirements.txt, render.yaml)
2. Modificar sqlite_api_clean.py para produção
3. Preparar o commit e push para GitHub
4. Te guiar passo a passo no Render

**O que você quer fazer primeiro?**
