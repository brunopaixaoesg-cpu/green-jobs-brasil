# ⚡ COMANDOS PRONTOS - COPIE E COLE

## 🚀 Teste Rápido (Windows PowerShell)

### Opção 1: Tudo de uma vez
```powershell
cd "C:\Users\Bruno\Empresas Verdes\scrapers_poc" ; pip install -r requirements.txt ; python test_scraper.py
```

### Opção 2: Passo a passo
```powershell
# Entrar na pasta
cd "C:\Users\Bruno\Empresas Verdes\scrapers_poc"

# Instalar dependências
pip install -r requirements.txt

# Executar teste
python test_scraper.py
```

---

## 📊 Ver Resultados

### Listar JSONs salvos
```powershell
dir results\*.json
```

### Abrir último JSON no VS Code
```powershell
code (Get-ChildItem results\*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
```

### Ver conteúdo no terminal
```powershell
Get-Content (Get-ChildItem results\*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Select-Object -ExpandProperty FullName) | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 🔧 Customizações Rápidas

### Buscar mais vagas (editar config.py)
```powershell
# Abrir config.py no VS Code
code config.py

# Depois mudar a linha:
# MAX_VAGAS_PER_RUN = 100  # Padrão: 50
```

### Adicionar nova keyword
```powershell
# Abrir config.py
code config.py

# Adicionar à lista ESG_KEYWORDS:
# "carbono zero",
# "energias limpas"
```

---

## 🧹 Limpar Resultados

### Deletar todos os JSONs
```powershell
Remove-Item results\*.json
```

### Deletar JSONs antigos (mais de 1 dia)
```powershell
Get-ChildItem results\*.json | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-1)} | Remove-Item
```

---

## 🐛 Troubleshooting

### Verificar se Python está instalado
```powershell
python --version
```

### Verificar pacotes instalados
```powershell
pip list | Select-String -Pattern "requests|beautifulsoup"
```

### Reinstalar dependências
```powershell
pip install -r requirements.txt --force-reinstall
```

### Testar conexão com Vagas.com
```powershell
Test-NetConnection vagas.com.br -Port 443
```

---

## 📁 Abrir Arquivos Rapidamente

### Abrir todos no VS Code
```powershell
code .
```

### Abrir documentação
```powershell
code README.md
code GUIA_RAPIDO.md
code RESUMO_EXECUTIVO.md
```

### Abrir código fonte
```powershell
code base_scraper.py
code vagas_com_scraper.py
code test_scraper.py
```

---

## ✅ COMANDO RECOMENDADO PARA PRIMEIRA VEZ

**Copie e cole este comando no PowerShell:**

```powershell
cd "C:\Users\Bruno\Empresas Verdes\scrapers_poc" ; Write-Host "`n🚀 Instalando dependências...`n" -ForegroundColor Green ; pip install -q -r requirements.txt ; Write-Host "`n✅ Instalação concluída!`n" -ForegroundColor Green ; Write-Host "📋 Iniciando teste do scraper...`n" -ForegroundColor Cyan ; python test_scraper.py
```

**O que faz:**
1. Entra na pasta do POC
2. Instala dependências silenciosamente
3. Mostra mensagens coloridas de progresso
4. Executa o teste

---

## 🎯 Pronto!

Agora é só copiar e colar! 🚀
