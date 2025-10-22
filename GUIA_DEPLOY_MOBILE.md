# 📱 Guia de Acesso Mobile Local - Green Jobs Brasil

## 🎯 Objetivo
Acessar a aplicação no celular através da rede local (Wi-Fi)

---

## ✅ Opção 1: Acesso pela Rede Local (MAIS RÁPIDO)

### Passo 1: Descobrir o IP do seu PC

**No PowerShell:**
```powershell
ipconfig
```

**Procure por**: `Adaptador de Rede sem Fio Wi-Fi`  
**Anote o**: `Endereço IPv4` (algo como `192.168.1.X`)

**Exemplo:**
```
Adaptador de Rede sem Fio Wi-Fi:
   Endereço IPv4: 192.168.1.105
```

### Passo 2: Modificar start_api.py para aceitar conexões externas

**Arquivo**: `start_api.py`

**Troque:**
```python
uvicorn.run("api.app:app", host="127.0.0.1", port=8002, reload=True)
```

**Por:**
```python
uvicorn.run("api.app:app", host="0.0.0.0", port=8002, reload=True)
```

> **0.0.0.0** = aceita conexões de qualquer IP na rede local

### Passo 3: Liberar Firewall do Windows

**No PowerShell como Administrador:**
```powershell
# Criar regra no firewall
New-NetFirewallRule -DisplayName "Green Jobs API" -Direction Inbound -LocalPort 8002 -Protocol TCP -Action Allow
```

**Ou manualmente:**
1. Windows Defender Firewall
2. Configurações Avançadas
3. Regras de Entrada → Nova Regra
4. Porta → TCP → 8002 → Permitir

### Passo 4: Reiniciar API

```powershell
py start_api.py
```

### Passo 5: Acessar no Celular

**Conecte o celular no MESMO Wi-Fi do PC**

**No navegador do celular:**
```
http://192.168.1.105:8002/api/profissionais/dashboard/1
```
(substitua 192.168.1.105 pelo SEU IP)

---

## ✅ Opção 2: Deploy em Servidor (PRODUÇÃO)

### 2A: Render.com (GRÁTIS - mais fácil)

**Vantagens:**
- ✅ Grátis para hobby projects
- ✅ Deploy automático via GitHub
- ✅ SSL/HTTPS automático
- ✅ URL pública (ex: greenjobs.onrender.com)

**Passos:**
1. Criar conta em https://render.com
2. Conectar repositório GitHub
3. Criar Web Service:
   - Build Command: `pip install -r api/requirements.txt`
   - Start Command: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`
4. Deploy automático!

**Limitações:**
- ❌ Sleep após 15min inatividade (demora 1min para "acordar")
- ❌ 512MB RAM (ok para MVP)
- ❌ Banco SQLite (não recomendado para produção)

---

### 2B: Railway.app (GRÁTIS com limites)

**Vantagens:**
- ✅ $5 crédito grátis/mês
- ✅ Deploy mais rápido que Render
- ✅ PostgreSQL grátis incluído
- ✅ Logs em tempo real

**Passos:**
1. Criar conta em https://railway.app
2. New Project → Deploy from GitHub
3. Add PostgreSQL (optional)
4. Configurar variáveis de ambiente
5. Deploy!

**Limitações:**
- ❌ Após $5 de uso, precisa pagar
- ❌ ~500 horas/mês grátis

---

### 2C: PythonAnywhere (GRÁTIS permanente)

**Vantagens:**
- ✅ 100% grátis para sempre
- ✅ Python nativo
- ✅ Fácil configuração
- ✅ Sempre online (sem sleep)

**Passos:**
1. Criar conta em https://www.pythonanywhere.com
2. Upload do código via Git ou interface
3. Configurar Web App (Flask/FastAPI)
4. URL: `yourusername.pythonanywhere.com`

**Limitações:**
- ❌ CPU limitada
- ❌ Subdomínio fixo (.pythonanywhere.com)
- ❌ Precisa upgrade ($5/mês) para domínio próprio

---

### 2D: Heroku (PAGO - mais confiável)

**Vantagens:**
- ✅ Muito estável
- ✅ PostgreSQL integrado
- ✅ Add-ons (Redis, ElasticSearch)
- ✅ CLI poderoso

**Passos:**
1. Criar conta em https://heroku.com
2. Instalar Heroku CLI
3. Criar app: `heroku create greenjobs-brasil`
4. Push: `git push heroku main`
5. Scale: `heroku ps:scale web=1`

**Custo:**
- ❌ $7/mês mínimo (dyno básico)
- ❌ Não tem free tier desde 2022

---

## ✅ Opção 3: Domínio + Hospedagem Própria

### 3A: VPS (DigitalOcean, Linode, Vultr)

**Custo:** $5-10/mês  
**Controle:** Total  
**Complexidade:** Alta (precisa configurar tudo)

**Passos:**
1. Alugar droplet/VPS Ubuntu
2. Instalar Python, PostgreSQL, Nginx
3. Configurar SSL (Let's Encrypt)
4. Deploy com systemd ou Docker
5. Apontar domínio

---

### 3B: Vercel (Frontend) + Render (Backend)

**Estratégia Híbrida:**
- Frontend (HTML/CSS/JS) → Vercel (grátis, super rápido)
- Backend (FastAPI) → Render (grátis com sleep)
- Banco → Supabase ou PlanetScale (grátis)

**Vantagens:**
- ✅ CDN global (Vercel)
- ✅ Frontend sempre rápido
- ✅ Separação de preocupações

---

## 📊 Comparação Rápida

| Opção | Custo | Dificuldade | Uptime | Speed | SSL |
|-------|-------|-------------|--------|-------|-----|
| **Rede Local** | Grátis | ⭐ Fácil | 🔴 PC ligado | 🟢 Rápido | ❌ |
| **Render** | Grátis | ⭐⭐ Médio | 🟡 Com sleep | 🟢 Bom | ✅ |
| **Railway** | $5/mês | ⭐⭐ Médio | 🟢 Sempre | 🟢 Bom | ✅ |
| **PythonAnywhere** | Grátis | ⭐⭐ Médio | 🟢 Sempre | 🟡 OK | ✅ |
| **Heroku** | $7/mês | ⭐⭐ Médio | 🟢 Sempre | 🟢 Bom | ✅ |
| **VPS** | $5-10/mês | ⭐⭐⭐⭐ Difícil | 🟢 Sempre | 🟢 Ótimo | ✅ |

---

## 🎯 Recomendação por Caso de Uso

### **Teste Mobile Hoje (5 minutos)**
→ **Opção 1: Rede Local**

### **MVP para Apresentar (Grátis)**
→ **Render.com** ou **PythonAnywhere**

### **Piloto com Primeiros Clientes**
→ **Railway** ($5/mês) ou **VPS DigitalOcean**

### **Produção Escalável**
→ **VPS** + Docker + PostgreSQL + Nginx + Domínio

---

## 🚀 Próximos Passos Sugeridos

1. **Agora**: Testar no celular via rede local (5 min)
2. **Hoje**: Deploy no Render.com (30 min)
3. **Amanhã**: Registrar domínio + SSL
4. **Semana que vem**: Migrar para VPS se tiver tração

---

## 🔒 Checklist de Segurança para Produção

- [ ] Mudar SECRET_KEY (não usar default)
- [ ] Adicionar rate limiting (slowapi)
- [ ] CORS configurado corretamente
- [ ] Variáveis de ambiente (.env)
- [ ] PostgreSQL em vez de SQLite
- [ ] Backup automático do banco
- [ ] Logs centralizados
- [ ] Monitoramento (UptimeRobot)
- [ ] SSL/HTTPS ativo
- [ ] Sanitização de inputs

---

## 📱 QR Code para Acesso Rápido

Depois de configurar rede local, você pode gerar um QR Code:

**Python script:**
```python
import qrcode

# Substitua pelo seu IP
url = "http://192.168.1.105:8002/api/profissionais/dashboard/1"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_access.png")
print("QR Code gerado! Aponte a câmera do celular.")
```

---

**Qual opção você prefere testar primeiro?**
1. Rede local (5 min) - testar agora no celular
2. Deploy Render.com (30 min) - link público grátis
3. Outra opção?
