"""Popular profissional de teste para upload"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from api.db import get_db

conn = get_db()
cursor = conn.cursor()

# Verificar se já existe
cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
count = cursor.fetchone()[0]

print(f"📊 Profissionais existentes: {count}")

if count == 0:
    # Inserir profissional de teste
    cursor.execute("""
        INSERT INTO profissionais_esg (
            nome, email, area_atuacao, experiencia_anos,
            localizacao_cidade, localizacao_uf, status,
            nome_completo, cargo_atual, empresa_atual
        ) VALUES (
            'Maria Silva Santos',
            'maria.santos@email.com',
            'Meio Ambiente',
            5,
            'São Paulo',
            'SP',
            'ativo',
            'Maria Silva Santos',
            'Analista Ambiental Sênior',
            'EcoTech Soluções'
        )
    """)
    conn.commit()
    print("✅ Profissional Maria Silva Santos criado com ID 1")
else:
    # Verificar se ID 1 existe
    cursor.execute("SELECT id, nome FROM profissionais_esg WHERE id = 1")
    prof = cursor.fetchone()
    if prof:
        print(f"✅ Profissional ID 1 já existe: {prof['nome']}")
    else:
        print("⚠️  ID 1 não existe, mas há outros profissionais")

conn.close()
