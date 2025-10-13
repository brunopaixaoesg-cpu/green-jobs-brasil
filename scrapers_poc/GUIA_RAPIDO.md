# 🚀 GUIA RÁPIDO - POC Scraper de Vagas ESG

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar dependências

```bash
cd scrapers_poc
pip install -r requirements.txt
```

### 2️⃣ Executar teste

```bash
python test_scraper.py
```

### 3️⃣ Ver resultados

Os resultados são salvos em `results/vagas_vagas.com_YYYY-MM-DD_HH-MM-SS.json`

---

## 📋 O que vai acontecer

1. **Confirmação**: Script pede confirmação antes de iniciar
2. **Scraping**: Busca vagas em Vagas.com usando 15 keywords ESG
3. **Progresso**: Mostra em tempo real quantas vagas foram encontradas
4. **Resumo**: Exibe estatísticas (total, por estado, por tipo, etc)
5. **Salvamento**: Grava JSON com todos os dados
6. **Detalhes opcionais**: Pergunta se quer buscar dados completos das 5 primeiras vagas

---

## 🎯 Exemplo de Output Esperado

```
======================================================================
🤖 POC - SCRAPER DE VAGAS ESG
======================================================================

📍 Fonte: Vagas.com
🔑 Keywords: 15
🎯 Meta: 50 vagas

Deseja continuar? (s/n): s

======================================================================

🔍 Iniciando scraping em vagas.com
📋 Keywords: 15
🎯 Meta: 50 vagas

  🔎 Buscando: 'sustentabilidade'...
    ✅ Encontradas: 12 vagas
  🔎 Buscando: 'ESG'...
    ✅ Encontradas: 8 vagas
  🔎 Buscando: 'meio ambiente'...
    ✅ Encontradas: 15 vagas
  ...

✅ Meta atingida! 50 vagas coletadas

📊 Resultado final:
   Total bruto: 52
   Duplicatas removidas: 2
   Total único: 50

============================================================
📊 RESUMO DO SCRAPING - VAGAS.COM
============================================================
✅ Total de vagas: 50
💰 Com informação salarial: 23
🏠 Vagas remotas: 18

📍 Por Estado:
   SP: 28
   RJ: 10
   MG: 6
   RS: 4
   PR: 2

📋 Por Tipo:
   CLT: 35
   PJ: 10
   Estágio: 5

💼 Primeiras 3 vagas:

   1. Analista de Sustentabilidade Pleno
      Empresa: Natura &Co
      Local: São Paulo - SP
      Link: https://www.vagas.com.br/vagas/v12345678...

   2. Coordenador ESG
      Empresa: Ambev
      Local: Rio de Janeiro - RJ  
      Link: https://www.vagas.com.br/vagas/v87654321...

   3. Especialista em Energia Renovável
      Empresa: Petrobras
      Local: Remoto
      Link: https://www.vagas.com.br/vagas/v11223344...

============================================================

💾 Resultados salvos em: results/vagas_vagas.com_2025-10-11_21-30-45.json

✅ Scraping concluído com sucesso!
📁 Arquivo salvo: results/vagas_vagas.com_2025-10-11_21-30-45.json
📊 Total de vagas: 50
```

---

## 🔧 Customização

### Mudar número de vagas
Edite `config.py`:
```python
MAX_VAGAS_PER_RUN = 100  # Padrão: 50
```

### Adicionar keywords
Edite `config.py`:
```python
ESG_KEYWORDS = [
    "sustentabilidade",
    "ESG",
    # Adicione mais aqui
    "carbono zero",
    "energias limpas"
]
```

### Ajustar delay (evitar bloqueio)
Edite `config.py`:
```python
REQUEST_DELAY = 3  # Padrão: 2 segundos
```

---

## ⚠️ Possíveis Problemas

### Nenhuma vaga encontrada
- **Causa**: HTML do site mudou
- **Solução**: Atualizar seletores CSS em `vagas_com_scraper.py`

### Bloqueio anti-scraping
- **Causa**: Muitas requisições rápidas
- **Solução**: Aumentar `REQUEST_DELAY` em `config.py`

### Timeout
- **Causa**: Conexão lenta
- **Solução**: Aumentar `REQUEST_TIMEOUT` em `config.py`

---

## 📊 Estrutura do JSON de Resultados

```json
{
  "fonte": "vagas.com",
  "data_scraping": "2025-10-11T21:30:45.123456",
  "total_vagas": 50,
  "keywords": ["sustentabilidade", "ESG", ...],
  "vagas": [
    {
      "titulo": "Analista de Sustentabilidade",
      "empresa": "Empresa Verde Ltda",
      "localizacao": "São Paulo - SP",
      "tipo": "CLT",
      "remoto": true,
      "descricao": "Descrição completa...",
      "requisitos": "Requisitos...",
      "salario": "R$ 6.000 - R$ 9.000",
      "link_candidatura": "https://...",
      "fonte": "vagas.com",
      "data_scraping": "2025-10-11T21:30:45",
      "keywords_encontradas": ["sustentabilidade"]
    }
  ]
}
```

---

## 🎯 Próximos Passos Após Teste

1. **Avaliar resultados**: Qualidade e quantidade das vagas
2. **Decidir integração**: Vale integrar no projeto principal?
3. **Se sim**: Mover para `Empresas Verdes/scrapers/`
4. **Se não**: Refinar POC ou buscar API paga

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se instalou todas as dependências
2. Teste sua conexão com `ping vagas.com.br`
3. Verifique os logs de erro
4. Consulte `README.md` para mais detalhes

---

**Criado por:** GitHub Copilot  
**Data:** 2025-10-11  
**Versão:** 1.0.0
