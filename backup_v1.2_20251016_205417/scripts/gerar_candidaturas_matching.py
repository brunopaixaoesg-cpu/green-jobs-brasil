#!/usr/bin/env python3
"""
Gerador de Candidaturas Para Testes de Matching
================================================
Cria candidaturas realísticas para testar o sistema de matching
entre profissionais ambientais e vagas específicas.
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Conectar ao banco
conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("🎯 Gerando Candidaturas de Teste para Matching")
print("=" * 50)

# 1. Buscar profissionais ambientais
cursor.execute("""
    SELECT id, nome_completo, cargo_atual 
    FROM profissionais_esg 
    WHERE cargo_atual LIKE '%Ambiental%' 
    OR cargo_atual LIKE '%EHS%'
    OR cargo_atual LIKE '%Meio Ambiente%'
    LIMIT 20
""")
profissionais = cursor.fetchall()

# 2. Buscar vagas ambientais  
cursor.execute("""
    SELECT id, titulo, nivel_experiencia
    FROM vagas_esg 
    WHERE titulo LIKE '%Ambiental%'
    OR titulo LIKE '%EHS%' 
    OR titulo LIKE '%Meio Ambiente%'
    LIMIT 15
""")
vagas = cursor.fetchall()

print(f"👥 Profissionais encontrados: {len(profissionais)}")
print(f"💼 Vagas encontradas: {len(vagas)}")

# 3. Criar tabela de candidaturas se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidaturas_esg (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profissional_id INTEGER,
        vaga_id INTEGER,
        data_candidatura DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'enviada',
        carta_motivacao TEXT,
        score_matching REAL DEFAULT 0.0,
        FOREIGN KEY (profissional_id) REFERENCES profissionais_esg (id),
        FOREIGN KEY (vaga_id) REFERENCES vagas_esg (id),
        UNIQUE(profissional_id, vaga_id)
    )
""")

# 4. Gerar candidaturas realísticas
candidaturas_criadas = 0
motivacoes = [
    "Tenho grande interesse em trabalhar com sustentabilidade e impacto ambiental positivo.",
    "Minha experiência em licenciamento ambiental seria muito útil para esta posição.",
    "Busco uma oportunidade para aplicar meus conhecimentos em gestão ambiental.",
    "Gostaria de contribuir com os objetivos de sustentabilidade da empresa.",
    "Tenho experiência prática em projetos de compliance ambiental.",
    "Esta vaga se alinha perfeitamente com minha carreira em ESG.",
    "Quero fazer parte de uma empresa comprometida com o meio ambiente."
]

for prof_id, prof_nome, prof_cargo in profissionais:
    # Cada profissional candidata-se a 2-5 vagas aleatórias
    num_candidaturas = random.randint(2, 5)
    vagas_escolhidas = random.sample(vagas, min(num_candidaturas, len(vagas)))
    
    for vaga_id, vaga_titulo, vaga_nivel in vagas_escolhidas:
        try:
            # Score baseado na compatibilidade simulada
            score = random.uniform(45.0, 95.0)
            
            # Ajustar score baseado na compatibilidade de nível
            if prof_cargo.lower() in vaga_titulo.lower():
                score += 10  # Bonus por compatibilidade de função
            
            if 'senior' in prof_cargo.lower() and 'senior' in vaga_nivel.lower():
                score += 15
            elif 'junior' in prof_cargo.lower() and 'junior' in vaga_nivel.lower():
                score += 15
            elif 'pleno' in prof_cargo.lower() and 'pleno' in vaga_nivel.lower():
                score += 15
            
            score = min(score, 98.0)  # Limitar a 98%
            
            cursor.execute("""
                INSERT OR IGNORE INTO candidaturas_esg 
                (profissional_id, vaga_id, observacoes, compatibilidade_score)
                VALUES (?, ?, ?, ?)
            """, (prof_id, vaga_id, random.choice(motivacoes), score))
            
            if cursor.rowcount > 0:
                candidaturas_criadas += 1
                print(f"✅ {prof_nome[:20]:<20} → {vaga_titulo[:30]:<30} (Score: {score:.1f}%)")
        
        except sqlite3.IntegrityError:
            # Candidatura já existe
            pass

conn.commit()

# 5. Estatísticas finais
cursor.execute("SELECT COUNT(*) FROM candidaturas_esg")
total_candidaturas = cursor.fetchone()[0]

cursor.execute("SELECT AVG(compatibilidade_score) FROM candidaturas_esg")
score_medio = cursor.fetchone()[0] or 0

print("\n" + "=" * 50)
print("🎉 CANDIDATURAS CRIADAS COM SUCESSO!")
print(f"✅ Novas candidaturas: {candidaturas_criadas}")
print(f"📊 Total no sistema: {total_candidaturas}")
print(f"💯 Score médio: {score_medio:.1f}%")
print("\n🔗 Agora você pode testar:")
print("   http://127.0.0.1:8000/matching/empresa")
print("   http://127.0.0.1:8000/matching/profissional")

conn.close()