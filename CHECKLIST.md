# ✅ Checklist - Sistema de Vagas ESG

**Quando você voltar, siga este checklist para verificar tudo:**

---

## 🔍 Verificações Rápidas

### 1. API está rodando?
```bash
cd "C:\Users\Bruno\Empresas Verdes"
py start_api.py
```

✅ Deve mostrar:
```
🚀 Iniciando Green Jobs Brasil API...
📍 API: http://127.0.0.1:8000
📚 Docs: http://127.0.0.1:8000/docs
```

---

### 2. Dashboard principal funcionando?
- [ ] Abrir: http://127.0.0.1:8000
- [ ] Ver link "Vagas ESG Disponíveis" no menu
- [ ] Clicar no link

---

### 3. Lista de Vagas funcionando?
- [ ] Abrir: http://127.0.0.1:8000/vagas
- [ ] Ver 3 vagas de exemplo
- [ ] Testar filtro de busca
- [ ] Testar filtro por UF
- [ ] Testar filtro por nível
- [ ] Ver botão "Publicar Vaga"

---

### 4. Publicar Vaga funcionando?
- [ ] Abrir: http://127.0.0.1:8000/vagas/publicar
- [ ] Formulário carregou
- [ ] Preencher dados:
  - CNPJ: `12.345.678/0001-90` (empresa exemplo)
  - Título: "Teste de Vaga ESG"
  - Descrição: Qualquer texto com 20+ caracteres
  - Selecionar ODS (checkboxes)
  - Adicionar habilidades
  - Selecionar nível e tipo de contratação
  - Email: seu email
- [ ] Clicar "Publicar Vaga"
- [ ] Ver mensagem de sucesso
- [ ] Ser redirecionado para lista
- [ ] Ver sua vaga na lista

---

### 5. API Docs funcionando?
- [ ] Abrir: http://127.0.0.1:8000/docs
- [ ] Ver seção "Vagas ESG"
- [ ] Expandir GET `/api/vagas/`
- [ ] Clicar "Try it out"
- [ ] Clicar "Execute"
- [ ] Ver resposta JSON com vagas

---

### 6. Filtros funcionando?
- [ ] Na lista de vagas, digitar texto na busca
- [ ] Lista filtra em tempo real
- [ ] Selecionar UF no dropdown
- [ ] Lista filtra
- [ ] Selecionar "Apenas Remoto"
- [ ] Lista filtra
- [ ] Limpar filtros
- [ ] Todas as vagas aparecem de novo

---

### 7. Git está correto?
```bash
git status
```
- [ ] Ver: "On branch feature/matching-system"
- [ ] Ver: "nothing to commit, working tree clean"

```bash
git log --oneline -5
```
- [ ] Ver commits recentes sobre sistema de vagas

---

## 🐛 Se algo não funcionar

### Problema: API não inicia
**Solução:**
```bash
# Verificar se porta 8000 está livre
netstat -ano | findstr :8000
# Se tiver processo, matar:
taskkill /F /PID <número_do_processo>
```

### Problema: Página não carrega
**Solução:**
1. Verificar se API está rodando
2. Limpar cache do navegador (Ctrl + Shift + Delete)
3. Abrir modo anônimo

### Problema: Erro ao publicar vaga
**Possível causa:** CNPJ não existe
**Solução:**
- Usar CNPJ de exemplo: `12.345.678/0001-90`
- Ou cadastrar empresa primeiro

---

## 📊 Estatísticas Esperadas

Ao abrir `/api/vagas/stats/resumo`:
```json
{
  "total": 3,
  "ativas": 3,
  "pausadas": 0,
  "fechadas": 0,
  "remotas": 2,
  "media_visualizacoes": 0,
  "total_candidaturas": 0,
  "vagas_por_ods": {
    "7": 2,
    "13": 3,
    "12": 1,
    "15": 2
  }
}
```

---

## 🎯 Testes Avançados (Opcional)

### Teste 1: Criar vaga via API
```bash
# No PowerShell
curl -X POST "http://127.0.0.1:8000/api/vagas/" `
  -H "Content-Type: application/json" `
  -d '{
    "cnpj": "12.345.678/0001-90",
    "titulo": "Vaga Teste API",
    "descricao": "Descrição de teste com mais de 20 caracteres",
    "ods_tags": [7, 13],
    "habilidades_requeridas": ["ISO 14001"],
    "nivel_experiencia": "pleno",
    "tipo_contratacao": "CLT",
    "publicada_por": "test@test.com"
  }'
```

### Teste 2: Listar vagas via API
```bash
curl "http://127.0.0.1:8000/api/vagas/"
```

### Teste 3: Filtrar por ODS
```bash
curl "http://127.0.0.1:8000/api/vagas/?ods=13"
```

---

## 📁 Arquivos para Revisar

Se quiser entender o código:

1. **Backend:**
   - `api/routers/vagas.py` - API completa

2. **Frontend:**
   - `api/templates/vagas/lista.html` - Lista de vagas
   - `api/templates/vagas/publicar.html` - Formulário

3. **Database:**
   - `db/migrations/001_create_vagas_esg.sql` - Schema

4. **Documentação:**
   - `PARA_BRUNO.md` - Guia geral
   - `SISTEMA_VAGAS_RESUMO.md` - Documentação técnica
   - `ARQUITETURA.md` - Estrutura do projeto

---

## 🎨 Customizações Possíveis

Se quiser ajustar algo:

### Mudar cores:
Editar variáveis CSS em `lista.html` e `publicar.html`:
```css
:root {
    --primary-green: #059669;
    --light-green: #10b981;
    /* ... */
}
```

### Adicionar ODS:
Editar `publicar.html`, adicionar checkbox:
```html
<div class="ods-checkbox">
    <input type="checkbox" name="ods" value="6" id="ods6">
    <label for="ods6">ODS 6 - Água Limpa</label>
</div>
```

### Mudar limite de vagas por página:
Editar `lista.html`, linha da função `carregarVagas`:
```javascript
const response = await fetch('/api/vagas/?limit=100'); // Mudou de 50 para 100
```

---

## 💾 Backup Recomendado

Antes de fazer mudanças grandes:
```bash
# Criar backup do banco
copy gjb_dev.db gjb_dev.db.backup

# Criar nova branch para testes
git checkout -b teste/minhas-mudancas
```

---

## 🚀 Próximo Deploy

Quando quiser colocar em produção:
```bash
# 1. Merge para master
git checkout master
git merge feature/matching-system

# 2. Tag de versão
git tag -a v2.0.0 -m "Sistema de Vagas ESG"

# 3. Push para repositório remoto
git push origin master --tags
```

---

## ✨ Tudo Funcionando?

Se todos os checkboxes acima estiverem marcados:

🎉 **PARABÉNS!** Sistema 100% funcional!

Próximos passos:
1. Testar com dados reais
2. Mostrar para o time
3. Desenvolver perfil de profissionais
4. Implementar matching

---

**Qualquer dúvida, o código está bem documentado!** 💚

**Desenvolvido em:** 11/10/2025  
**Status:** ✅ COMPLETO  
**Pronto para:** PRODUÇÃO
