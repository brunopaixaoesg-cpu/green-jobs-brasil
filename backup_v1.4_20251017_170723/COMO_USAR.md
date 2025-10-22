# 🚀 GUIA RÁPIDO - GJB System v1.2

## Para Iniciar o Sistema (SEM VS CODE):

### Opção 1: Duplo-clique no arquivo
```
📁 INICIAR_SISTEMA.bat
```
→ Clique 2x no arquivo e pronto!

### Opção 2: Pelo PowerShell/CMD
```powershell
# Entrar na pasta
cd "C:\Users\Bruno\Empresas Verdes"

# Iniciar sistema
py start_api.py
```

### Opção 3: Direto com Python
```powershell
cd "C:\Users\Bruno\Empresas Verdes"
py api/sqlite_api_clean.py
```

## 🌐 Acessar o Sistema

Após iniciar, abra o navegador em:

- **Página Principal**: http://127.0.0.1:8002/
- **Dashboard**: http://127.0.0.1:8002/dashboard
- **Empresas**: http://127.0.0.1:8002/empresas
- **Vagas**: http://127.0.0.1:8002/vagas
- **Profissionais**: http://127.0.0.1:8002/profissionais
- **ML Dashboard**: http://127.0.0.1:8002/ml-avancado
- **Documentação API**: http://127.0.0.1:8002/docs

## 🧪 Testar o Sistema

### Teste Rápido (duplo-clique):
```
📁 TESTAR_SISTEMA.bat
```

### Teste Manual:
```powershell
py teste_rapido.py
```

## 🛑 Parar o Sistema

- Pressione **Ctrl + C** no terminal
- Ou feche a janela do terminal

## 💾 Fazer Backup

```powershell
.\backup_v1.2.ps1
```

## 📊 Status do Sistema v1.2

- ✅ API FastAPI funcionando
- ✅ 7 páginas web operacionais
- ✅ 8 endpoints REST
- ✅ Banco de dados com 981 registros
- ✅ Sistema de matching com ML

## 🆘 Problemas?

1. **API não inicia**: Verifique se a porta 8002 está livre
2. **Erro de módulo**: Reinstale dependências: `pip install -r api/requirements.txt`
3. **Banco vazio**: Verifique se `gjb_dev.db` existe

## 📚 Documentação Completa

Para detalhes técnicos, consulte:
- `VERSION_1.2.md` - Documentação completa da versão
- `DOCUMENTACAO_COMPLETA.md` - Documentação técnica detalhada
- `MAPA_ROTAS.md` - Mapa de todas as rotas
