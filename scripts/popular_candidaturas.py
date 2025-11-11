"""Script para popular candidaturas no banco de dados"""
import sqlite3
import json
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('api/gjb_dev.db')
c = conn.cursor()

# Buscar profissionais e vagas existentes
c.execute("SELECT id, nome, email, area_atuacao, experiencia_anos FROM profissionais_esg")
profissionais = c.fetchall()

c.execute("SELECT id, titulo FROM vagas")
vagas = c.fetchall()

if not profissionais or not vagas:
    print("❌ Erro: É necessário ter profissionais e vagas no banco!")
    conn.close()
    exit(1)

print(f"📊 Encontrados: {len(profissionais)} profissionais e {len(vagas)} vagas")

# Criar candidaturas com scores variados
candidaturas = []
status_opcoes = ['nova', 'em_analise', 'aprovada', 'rejeitada']
habilidades_exemplo = [
    ["Python", "Machine Learning", "ESG"],
    ["Energia Solar", "Sustentabilidade", "Projetos"],
    ["Gestão Ambiental", "ISO 14001", "Relatórios"],
    ["Reciclagem", "Economia Circular", "Supply Chain"],
    ["Finanças Sustentáveis", "Green Bonds", "ESG Reporting"]
]

print("\n🔄 Criando candidaturas...")

for prof_id, nome, email, area, exp_anos in profissionais:
    # Cada profissional candidata para 2-3 vagas
    num_candidaturas = random.randint(2, 3)
    vagas_candidatadas = random.sample(vagas, min(num_candidaturas, len(vagas)))
    
    for vaga_id, vaga_titulo in vagas_candidatadas:
        # Gerar score baseado em experiência e aleatoriedade
        base_score = min(85, 50 + (exp_anos * 5))
        score = base_score + random.randint(-15, 15)
        score = max(30, min(100, score))  # Entre 30 e 100
        
        # Status baseado no score
        if score >= 85:
            status = 'aprovada'
        elif score >= 70:
            status = 'em_analise'
        elif score >= 50:
            status = 'nova'
        else:
            status = 'rejeitada'
        
        # Data de candidatura nos últimos 30 dias
        dias_atras = random.randint(1, 30)
        data_candidatura = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d %H:%M:%S')
        
        habilidades = json.dumps(random.choice(habilidades_exemplo))
        
        candidatura = (
            vaga_id,
            nome,
            email,
            random.choice(['(11) 98765-4321', '(21) 99876-5432', '(47) 91234-5678']),
            f"Currículo de {nome} com experiência em {area}. Atuação focada em sustentabilidade e ESG.",
            exp_anos,
            habilidades,
            f"Motivação para contribuir com impacto ambiental positivo e desenvolvimento sustentável na vaga de {vaga_titulo}.",
            score,
            status,
            data_candidatura
        )
        candidaturas.append(candidatura)

# Inserir candidaturas
c.executemany("""
    INSERT INTO candidaturas_esg (
        vaga_id, nome_completo, email, telefone, curriculo_texto,
        anos_experiencia_esg, habilidades_esg, motivacao,
        compatibilidade_score, status, data_candidatura
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", candidaturas)

conn.commit()

# Verificar resultado
c.execute("SELECT COUNT(*) FROM candidaturas_esg")
total = c.fetchone()[0]

c.execute("SELECT AVG(compatibilidade_score) FROM candidaturas_esg")
media = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM candidaturas_esg WHERE compatibilidade_score >= 85")
excelentes = c.fetchone()[0]

print(f"\n✅ Criadas {total} candidaturas!")
print(f"📊 Score médio: {media:.1f}")
print(f"⭐ Matches excelentes (≥85): {excelentes}")

conn.close()
print("\n🎉 Candidaturas populadas com sucesso!")
