# 🌱 Green Jobs Brasil - Guia para Dados Reais

## Como Funcionar com Milhares de Empresas Reais

### 📋 Visão Geral
Este guia explica como expandir o sistema Green Jobs Brasil de 10 empresas exemplo para milhares de empresas reais usando dados da Receita Federal e APIs públicas.

## 🎯 Estratégias de Implementação

### 1. **Busca Individual por CNPJ** ⭐ RECOMENDADO
```bash
python search_company.py
```

**Como funciona:**
- Digite um CNPJ de qualquer empresa brasileira
- O sistema busca na Receita Federal via API
- Analisa os CNAEs da empresa
- Calcula automaticamente se é "verde" ou não
- Salva no banco se for verde

**Exemplo de uso:**
```
🔍 Buscando empresa com CNPJ: 34.028.316/0001-96
==========================================================
🌐 Buscando na Receita Federal...

📊 RESULTADO DA ANÁLISE:
   Nome: COMPANHIA DE BEBIDAS DAS AMERICAS - AMBEV
   CNPJ: 34.028.316/0001-96
   Score Verde: 0/100
   ❌ Empresa NÃO é verde
```

### 2. **Importação em Massa**
```bash
python mass_import.py
```

**Opções disponíveis:**
- Setores prioritários (energia, reciclagem, ambiental)
- Importação por estado/região
- Download completo da Receita Federal

### 3. **Integração com Bases Públicas**

#### **Receita Federal - CNPJ Aberto**
- **URL**: http://200.152.38.155/CNPJ/dados_abertos_cnpj/
- **Dados**: Todos os CNPJs ativos do Brasil (~50 milhões)
- **Formato**: CSV separado por vírgulas
- **Tamanho**: ~15GB compactado

#### **APIs Públicas Recomendadas**
1. **ReceitaWS** (Gratuita com limite)
   - URL: https://www.receitaws.com.br/
   - Limite: 3 consultas/minuto
   - Dados: CNPJ, CNAEs, endereço, situação

2. **BrasilAPI** (Gratuita)
   - URL: https://brasilapi.com.br/
   - Limite: Mais generoso
   - Dados: CNPJs, CEPs, bancos

3. **Serasa Experian** (Comercial)
   - Dados mais completos
   - Informações financeiras
   - Histórico creditício

## 🏭 Como Identificar Empresas Verdes

### Critérios de Classificação

#### **CNAEs Verdes (43 códigos identificados)**
```python
# Exemplos de CNAEs verdes no sistema:
"35.11-5": "Geração de energia elétrica",      # CORE
"38.11-4": "Coleta de resíduos não-perigosos", # CORE  
"71.12-1": "Serviços de engenharia",           # ADJACENT
"84.13-4": "Administração pública ambiental",  # CORE
```

#### **Sistema de Pontuação**
- **Core (100 pontos)**: Atividade principal verde
- **Adjacent (70 pontos)**: Atividade relacionada
- **Secondary (40 pontos)**: Potencial verde
- **Bonus**: +20 pontos se >50% dos CNAEs são verdes

### Algoritmo de Classificação
```python
def calculate_green_score(cnaes):
    total_score = 0
    for cnae in cnaes:
        if cnae in green_cnaes_core:
            total_score += 100
        elif cnae in green_cnaes_adjacent:
            total_score += 70
        elif cnae in green_cnaes_secondary:
            total_score += 40
    
    return min(100, total_score / len(cnaes))
```

## 📊 Processamento em Escala

### Para Milhares de Empresas

#### **Método 1: Processamento por Lotes**
```python
# Exemplo: 1000 CNPJs por vez
cnpj_list = ["12.345.678/0001-90", "98.765.432/0001-01", ...]
processor = RealDataProcessor()
green_companies = processor.process_cnpj_list(cnpj_list)
processor.save_green_companies(green_companies)
```

#### **Método 2: Filtro por Setores**
```python
# Focar em setores com maior probabilidade
priority_sectors = [
    "35",  # Eletricidade e gás
    "38",  # Coleta e tratamento de resíduos
    "71",  # Atividades técnicas e científicas
    "84",  # Administração pública
]
```

#### **Método 3: Processamento Regional**
```python
# Processar por estado para otimizar
estados = ["SP", "RJ", "MG", "RS", "PR"]
for uf in estados:
    process_companies_by_state(uf)
```

## 🚀 Implementação Prática

### Passo a Passo para Produção

#### **1. Configurar Ambiente**
```bash
# Instalar dependências
pip install requests pandas sqlalchemy fastapi

# Verificar conectividade
python -c "import requests; print('OK')"
```

#### **2. Testar com Empresas Conhecidas**
```bash
# Empresas que sabemos que são verdes
python search_company.py
# Digite: 04.814.563/0001-74 (WEG - energia)
```

#### **3. Expandir Gradualmente**
```bash
# Começar com 100 empresas
python mass_import.py
# Escolher opção 1: Setores prioritários
```

#### **4. Monitorar Performance**
```bash
# Verificar resultados
python -c "
import sqlite3
conn = sqlite3.connect('gjb_dev.db')
print('Total empresas:', conn.execute('SELECT COUNT(*) FROM empresas_verdes').fetchone()[0])
conn.close()
"
```

### Otimizações para Escala

#### **Cache de Consultas**
```python
# Evitar consultas duplicadas
processed_cnpjs = set()
if cnpj not in processed_cnpjs:
    process_company(cnpj)
    processed_cnpjs.add(cnpj)
```

#### **Rate Limiting**
```python
import time
time.sleep(1)  # 1 segundo entre consultas
```

#### **Processamento Paralelo**
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_company, cnpj_list)
```

## 📈 Resultados Esperados

### Por Setor (Estimativas)
- **Energia Renovável**: ~500-1000 empresas
- **Gestão de Resíduos**: ~200-500 empresas  
- **Consultoria Ambiental**: ~1000-2000 empresas
- **Agricultura Sustentável**: ~300-800 empresas
- **Transporte Limpo**: ~100-300 empresas

### Por Região
- **Sudeste (SP/RJ/MG)**: ~60% das empresas verdes
- **Sul (RS/SC/PR)**: ~20% das empresas verdes
- **Nordeste**: ~15% das empresas verdes
- **Outros**: ~5% das empresas verdes

## 🔧 Troubleshooting

### Problemas Comuns

#### **Erro de Rate Limit**
```
Solução: Aumentar delay entre consultas
time.sleep(2)  # 2 segundos
```

#### **CNPJ Não Encontrado**
```
Causa: CNPJ inativo ou inválido
Solução: Verificar status na Receita Federal
```

#### **Score Zero**
```
Causa: Empresa não tem CNAEs verdes
Solução: Normal, nem toda empresa é verde
```

## 📞 Suporte

### Para Implementação Completa
1. Contatar Receita Federal para acesso aos dados completos
2. Considerar APIs comerciais para dados mais ricos
3. Implementar cache/banco mais robusto (PostgreSQL)
4. Adicionar validações de CNPJ mais rigorosas

### Próximos Passos
- Integração com dados de sustentabilidade
- Machine Learning para classificação automática
- Dashboard com analytics avançados
- API pública para terceiros

---

**✅ Sistema pronto para escalar de 10 para milhares de empresas!**