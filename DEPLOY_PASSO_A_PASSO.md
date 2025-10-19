# 🚀 GUIA DE DEPLOY - Green Jobs Brasil no Render.com

**Data**: 19/10/2025  
**Objetivo**: Colocar o MVP online em 30 minutos

---

## ✅ Arquivos Preparados

- ✅ `requirements.txt` - Dependências Python
- ✅ `.gitignore` - Arquivos para ignorar no Git
- ✅ `api/sqlite_api_clean.py` - Modificado para aceitar PORT

---

## 📋 Passo a Passo

### **Passo 1: Verificar se Git está inicializado** (5 min)

```powershell
cd "C:\Users\Bruno\Empresas Verdes"
git status
```

**Se der erro "not a git repository":**
```powershell
git init
git add .
git commit -m "Initial commit - Green Jobs Brasil MVP v1.0"
```

**Se já estiver inicializado:**
```powershell
git add .
git commit -m "Preparando deploy para Render.com"
```

---

### **Passo 2: Criar Repositório no GitHub** (5 min)

1. Acesse: https://github.com/new
2. **Repository name**: `green-jobs-brasil`
3. **Description**: `Plataforma de empregos ESG com Storytelling e ML - MVP`
4. **Visibilidade**: Público (para Render free tier funcionar)
5. **NÃO** marque "Initialize with README"
6. Clique em **"Create repository"**

---

### **Passo 3: Fazer Push para GitHub** (2 min)

Copie os comandos que aparecem no GitHub (algo como):

```powershell
git remote add origin https://github.com/SEU_USUARIO/green-jobs-brasil.git
git branch -M main
git push -u origin main
```

**⚠️ Importante**: Substitua `SEU_USUARIO` pelo seu username do GitHub!

**Se pedir login:**
- Username: seu username do GitHub
- Password: use um **Personal Access Token** (não a senha)
  - Criar token: https://github.com/settings/tokens
  - Permissões: `repo` (full control)

---

### **Passo 4: Criar Conta no Render.com** (3 min)

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. **Login com GitHub** (recomendado)
4. Autorize o Render a acessar seus repositórios

---

### **Passo 5: Criar Web Service** (10 min)

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório:
   - Se não aparecer, clique em **"Configure account"** e autorize
   - Selecione `green-jobs-brasil`
4. Configurações:

**Nome do Serviço:**
```
greenjobs-brasil
```
(Este será seu subdomínio: greenjobs-brasil.onrender.com)

**Region:**
```
Oregon (US West)
```
(ou Frankfurt se preferir Europa)

**Branch:**
```
main
```

**Root Directory:**
```
(deixar vazio)
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python api/sqlite_api_clean.py
```

**Instance Type:**
```
Free
```

5. **Environment Variables** (opcional por enquanto):
   - Pode adicionar depois se precisar

6. Clique em **"Create Web Service"**

---

### **Passo 6: Aguardar Deploy** (5-10 min)

O Render vai:
1. ⏳ Clonar seu repositório
2. ⏳ Instalar dependências (`pip install -r requirements.txt`)
3. ⏳ Iniciar a aplicação
4. ✅ Status mudará para **"Live"**

**Acompanhe os logs** na interface do Render para ver o progresso.

---

### **Passo 7: Testar a Aplicação** (2 min)

Quando status = **"Live"**, sua URL será:

```
https://greenjobs-brasil.onrender.com
```

**Teste:**

- **Landing Page**: https://greenjobs-brasil.onrender.com/
- **API Docs**: https://greenjobs-brasil.onrender.com/docs
- **Dashboard**: https://greenjobs-brasil.onrender.com/api/profissionais/dashboard/1
- **Perfil**: https://greenjobs-brasil.onrender.com/api/profissionais/perfil/1

**No celular:**
Abra o navegador e acesse diretamente a URL (sem precisar de Wi-Fi local!)

---

## 🎯 Pronto! Seu MVP está ONLINE!

### **URLs Importantes:**

```
🌐 Site: https://greenjobs-brasil.onrender.com
📄 API: https://greenjobs-brasil.onrender.com/docs
👤 Perfil Maria: https://greenjobs-brasil.onrender.com/api/profissionais/perfil/1
👤 Perfil João: https://greenjobs-brasil.onrender.com/api/profissionais/perfil/2
👤 Perfil Ana: https://greenjobs-brasil.onrender.com/api/profissionais/perfil/3
👤 Perfil Carlos: https://greenjobs-brasil.onrender.com/api/profissionais/perfil/4
```

---

## ⚠️ Limitações do Free Tier

### **Sleep após 15 minutos de inatividade**
- Primeira requisição demora ~30s para "acordar"
- Requisições seguintes são normais

**Solução 1: Aceitar** (ok para MVP/testes)

**Solução 2: Keep-alive** com UptimeRobot (grátis):
1. Criar conta: https://uptimerobot.com
2. Add Monitor → HTTP(s)
3. URL: sua URL do Render
4. Interval: 5 minutes
5. O UptimeRobot faz ping a cada 5min, mantendo app acordado

**Solução 3: Upgrade** para $7/mês (sem sleep)

---

## 🔧 Troubleshooting

### **Erro: Application failed to respond**
- Verifique **Start Command**: `python api/sqlite_api_clean.py`
- Verifique logs: pode ser falta de dependência

### **Erro 404 em todas as rotas**
- Verifique se `api/sqlite_api_clean.py` está no caminho correto
- Verifique se routers estão sendo importados

### **Banco de dados vazio**
- Normal! O `gjb_dev.db` está no `.gitignore`
- Render vai criar um banco novo vazio
- **Solução temporária**: Remover `*.db` do `.gitignore` e fazer commit
- **Solução permanente**: Migrar para PostgreSQL (tutorial separado)

### **App reinicia sozinho**
- Normal! Render reinicia a cada deploy
- SQLite em disco efêmero = dados perdidos
- Use PostgreSQL para produção

---

## 📊 Próximos Passos Recomendados

### **Curto Prazo (hoje):**
1. ✅ Testar todas as páginas online
2. ✅ Compartilhar URL com amigos/potenciais usuários
3. ✅ Coletar feedback inicial

### **Médio Prazo (semana):**
1. 🗄️ Migrar para PostgreSQL (Render oferece free tier)
2. 🎨 Adicionar domínio customizado (greenjobs.com.br)
3. 📧 Configurar email notifications
4. 📊 Adicionar Google Analytics

### **Longo Prazo (mês):**
1. 💰 Implementar sistema de pagamento (vagas)
2. 🕷️ Scraping de empresas reais
3. 📱 PWA completo com service worker
4. 🚀 Escalabilidade (VPS ou upgrade Render)

---

## 🎉 Checklist Final

- [ ] Git inicializado e commit feito
- [ ] Repositório criado no GitHub
- [ ] Push para GitHub OK
- [ ] Conta Render.com criada
- [ ] Web Service criado
- [ ] Deploy concluído (status "Live")
- [ ] URL acessível
- [ ] Testado no desktop
- [ ] Testado no celular
- [ ] Compartilhado com primeiros usuários

---

## 📱 QR Code para Compartilhar

Depois do deploy, você pode gerar QR Code da URL pública:

```python
import qrcode

url = "https://greenjobs-brasil.onrender.com/api/profissionais/perfil/1"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="green", back_color="white")
img.save("qr_green_jobs_online.png")
```

---

## 💡 Dicas de Uso

### **Para Apresentar:**
1. Comece pela landing page
2. Mostre um perfil storytelling (João ou Ana)
3. Demonstre o formulário de edição
4. Mostre o dashboard empresa
5. Destaque o diferencial ESG + ML

### **Para Pitch:**
- "Única plataforma de empregos ESG com storytelling visual no Brasil"
- "Mobile-first desde o início (60% dos acessos são mobile)"
- "ML realista, não promessas falsas de 90%+"
- "4 perfis já criados com projetos reais de impacto"

---

**Boa sorte com o deploy! 🚀**

Se tiver qualquer problema, consulte os logs do Render ou me avise!
