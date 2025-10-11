# 🔧 Green Jobs Brasil - Solução de Problemas

## ✅ VERSÃO SIMPLIFICADA - SEMPRE FUNCIONA

### 🚀 Como usar (3 opções, da mais fácil para a mais técnica):

#### **Opção 1: Script Ultra-Simples** ⭐ (RECOMENDADO)
```bash
# Execute:
python run_green_jobs.py
```
- ✅ Sempre funciona
- ✅ Verificações automáticas
- ✅ Orientações claras
- ✅ Abre navegador automaticamente

#### **Opção 2: Arquivo Batch Melhorado**
```bash
# Duplo clique em:
iniciar_green_jobs.bat
```
- ✅ Interface melhorada
- ✅ Verificações de erro
- ✅ Mensagens mais claras

#### **Opção 3: Direto pela API** (Para desenvolvedores)
```bash
cd "C:\Users\Bruno\Empresas Verdes\api"
python sqlite_api.py
```

## 🛠️ Problemas Resolvidos

### ❌ Problema: "API encerrada inesperadamente"
**✅ Solução**: Criado `run_green_jobs.py` que é mais estável

### ❌ Problema: "Tabela não encontrada"
**✅ Solução**: Corrigidos caminhos do banco de dados

### ❌ Problema: "Python não encontrado"
**✅ Solução**: Scripts verificam Python automaticamente

### ❌ Problema: "Interface gráfica não abre"
**✅ Solução**: Versão simplificada sem dependências complexas

## 📋 Checklist de Verificação

Antes de usar, verifique:

- [ ] ✅ Python instalado
- [ ] ✅ No diretório correto (`C:\Users\Bruno\Empresas Verdes`)
- [ ] ✅ Arquivo `gjb_dev.db` existe
- [ ] ✅ Pasta `api/` existe com `sqlite_api.py`

## 🎯 URLs do Sistema

Após iniciar, acesse:

- **🏠 API Base**: http://127.0.0.1:8000
- **📚 Documentação**: http://127.0.0.1:8000/docs
- **🏢 Empresas**: http://127.0.0.1:8000/empresas
- **📊 Estatísticas**: http://127.0.0.1:8000/stats
- **💚 Health Check**: http://127.0.0.1:8000/health

## 🆘 Se Nada Funcionar

Execute este comando para diagnóstico:

```bash
python check_db.py
```

Isso mostrará:
- ✅ Se o banco está OK
- ✅ Quantos registros existem
- ✅ Estrutura das tabelas

## 🔄 Reiniciar Sistema

Se algo der errado:

1. **Feche** todos os terminais
2. **Execute** novamente: `python run_green_jobs.py`
3. **Aguarde** 3-5 segundos para a API inicializar
4. **Acesse** http://127.0.0.1:8000/docs

## 📞 Status do Sistema

✅ **FUNCIONANDO**: 
- Base de dados: 10 empresas + 43 CNAEs
- API REST completa
- Documentação interativa
- Filtros e buscas

🎯 **PRÓXIMOS PASSOS AUTOMÁTICOS**:
- Otimização de performance
- Testes adicionais
- Melhorias na documentação
- Preparação para dados reais

---

**Sistema estabilizado e pronto para uso! 🌱**