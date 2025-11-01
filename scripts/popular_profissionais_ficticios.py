
import csv
import random
from faker import Faker
from scripts.db_wrapper import get_connection

# Configurações
CSV_PATH = r'data/raw/Leads Profissionais Ambientais 20250123.csv'
DB_PATH = r'gjb_dev.db'

# Profissões fictícias
PROFISSOES = [
    'Engenheiro Ambiental', 'Gestor ESG', 'Analista de Sustentabilidade', 'Consultor de Meio Ambiente',
    'Biólogo', 'Geógrafo', 'Químico Ambiental', 'Especialista em Energia Limpa', 'Advogado Ambiental',
    'Gestor de Resíduos', 'Educador Ambiental', 'Auditor ESG', 'Coordenador de Projetos Verdes',
    'Tecnólogo em Saneamento', 'Analista de Mudanças Climáticas', 'Gestor de Recursos Hídricos',
    'Especialista em Biodiversidade', 'Consultor de Economia Circular', 'Engenheiro Florestal', 'Analista de Responsabilidade Social'
]

fake = Faker('pt_BR')

# Extrai cidades e UFs do CSV
cidades_ufs = set()
with open(CSV_PATH, encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        cidades_ufs.add((row['CIDADE'], row['UF']))

cidades_ufs = list(cidades_ufs)

# Gera profissionais fictícios
num_profissionais = min(5000, len(cidades_ufs) * 2)
with get_connection() as conn:
    cursor = conn.cursor()
    for i in range(num_profissionais):
        cidade, uf = random.choice(cidades_ufs)
        nome_completo = fake.name()
        email = fake.email()
        area_atuacao = random.choice(PROFISSOES)
        anos_experiencia_esg = random.randint(0, 20)
        cursor.execute('''
            INSERT INTO profissionais_esg (nome_completo, email, area_atuacao, anos_experiencia_esg, localizacao_cidade, localizacao_uf)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome_completo, email, area_atuacao, anos_experiencia_esg, cidade, uf))

    conn.commit()

print(f'Base fictícia de profissionais ESG criada com sucesso! Total: {num_profissionais}')
