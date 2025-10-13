"""
Configurações do Scraper de Vagas ESG
"""
import os

# Keywords ESG para busca
ESG_KEYWORDS = [
    "sustentabilidade",
    "ESG",
    "meio ambiente",
    "ambiental",
    "ODS",
    "energia renovável",
    "solar",
    "eólica",
    "reciclagem",
    "carbono neutro",
    "emissões",
    "economia circular",
    "biodiversidade",
    "green",
    "sustentável"
]

# ODS (para classificação futura)
ODS_MAPPING = {
    7: ["energia", "renovável", "solar", "eólica", "limpa"],
    8: ["emprego", "trabalho decente", "crescimento econômico"],
    9: ["inovação", "infraestrutura", "indústria"],
    11: ["cidades sustentáveis", "comunidades", "urbano"],
    12: ["consumo responsável", "produção sustentável", "economia circular"],
    13: ["clima", "mudanças climáticas", "carbono", "emissões", "GEE"],
    14: ["oceanos", "vida marinha", "água"],
    15: ["vida terrestre", "biodiversidade", "floresta", "desmatamento"]
}

# Headers HTTP (simular navegador)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Rate limiting (segundos entre requests)
REQUEST_DELAY = 2  # 2 segundos entre cada requisição

# Timeout (segundos)
REQUEST_TIMEOUT = 10

# Número máximo de vagas por scraping
MAX_VAGAS_PER_RUN = 50

# Diretório de resultados
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

# Criar diretório se não existir
os.makedirs(RESULTS_DIR, exist_ok=True)
