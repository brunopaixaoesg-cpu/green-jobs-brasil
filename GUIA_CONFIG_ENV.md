# 🔐 Guia de Configuração - Variáveis de Ambiente

## 📋 Setup Rápido

### 1. Copiar arquivo de exemplo
```bash
cp .env.example .env
```

### 2. Gerar SECRET_KEY segura
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Editar `.env` com seus valores
```bash
# Mínimo necessário para desenvolvimento:
PORT=8002
HOST=127.0.0.1
SECRET_KEY=<cole_aqui_a_chave_gerada>
DB_PATH=api/gjb_dev.db
```

### 4. Testar configuração
```bash
python api/config.py
```

Deve mostrar:
```
✅ Configuração válida!
```

---

## 🔧 Variáveis Principais

### **Obrigatórias**
| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `SECRET_KEY` | Chave para JWT e sessões | `<gerar_com_secrets>` |
| `DB_PATH` | Caminho do banco SQLite | `api/gjb_dev.db` |

### **Servidor**
| Variável | Default | Descrição |
|----------|---------|-----------|
| `PORT` | `8002` | Porta da API |
| `HOST` | `127.0.0.1` | Host da API |
| `DEBUG` | `true` | Modo debug |
| `RELOAD` | `true` | Auto-reload em dev |

### **Segurança**
| Variável | Default | Descrição |
|----------|---------|-----------|
| `CORS_ORIGINS` | `localhost:3000,...` | Origens permitidas (CSV) |
| `RATE_LIMIT_PER_SECOND` | `10` | Requisições por segundo |
| `JWT_EXPIRATION_MINUTES` | `1440` | Expiração do token (24h) |

### **Logging**
| Variável | Default | Descrição |
|----------|---------|-----------|
| `LOG_LEVEL` | `INFO` | DEBUG/INFO/WARNING/ERROR |
| `LOG_FORMAT` | `text` | text ou json |
| `LOG_MAX_SIZE_MB` | `10` | Tamanho máx do arquivo |

---

## 🚀 Uso

### Import no código
```python
from api.config import config

# Acessar variáveis
print(config.PORT)
print(config.SECRET_KEY)
print(config.get_cors_origins())
print(config.is_production())
```

### Validação automática
```python
errors = config.validate()
if errors:
    for error in errors:
        print(f"⚠️ {error}")
```

### Print configuração
```python
config.print_config()
```

---

## 🔒 Segurança

### ❌ **NUNCA** commite o arquivo `.env`
```bash
# Já está no .gitignore
.env
.env.local
```

### ✅ **Sempre** gere SECRET_KEY única
```python
import secrets
print(secrets.token_urlsafe(32))
# Exemplo: dFLjfK3mP_vN2QxR8yWz1aB4cE5tU6hI7jK8lM9nO0p
```

### ⚠️ **Produção**
- Use `ENVIRONMENT=production`
- Defina `SECRET_KEY` forte
- Configure `DATABASE_URL` (PostgreSQL)
- Remova localhost/127.0.0.1 de `CORS_ORIGINS`
- Defina `DEBUG=false` e `RELOAD=false`

---

## 🧪 Testes

### Teste manual
```bash
# Ver configuração atual
python api/config.py

# Validar
python api/config.py && echo "OK" || echo "ERRO"
```

### Teste com variáveis customizadas
```bash
# Windows PowerShell
$env:PORT="8003"; python api/config.py

# Linux/Mac
PORT=8003 python api/config.py
```

---

## 📚 Referências

- **python-dotenv**: https://pypi.org/project/python-dotenv/
- **secrets module**: https://docs.python.org/3/library/secrets.html
- **FastAPI Config**: https://fastapi.tiangolo.com/advanced/settings/

---

## ❓ FAQ

**P: Como usar PostgreSQL em produção?**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/greenjobs
```

**P: Como desabilitar rate limiting?**
```env
RATE_LIMIT_PER_SECOND=999999
```

**P: Como habilitar JSON logs?**
```env
LOG_FORMAT=json
```

**P: Como adicionar nova variável?**
1. Adicione em `.env.example`
2. Adicione na classe `Config` em `api/config.py`
3. Documente aqui
