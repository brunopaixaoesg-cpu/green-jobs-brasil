"""Script para criar tabela empresas_esg com autenticação"""
import sqlite3
import hashlib
from datetime import datetime

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Criar tabela empresas_esg
cursor.execute("""
CREATE TABLE IF NOT EXISTS empresas_esg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnpj TEXT UNIQUE NOT NULL,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    telefone TEXT,
    cidade TEXT,
    estado TEXT,
    setor TEXT,
    descricao TEXT,
    logo_url TEXT,
    site TEXT,
    status TEXT DEFAULT 'ativa',
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

print("✅ Tabela empresas_esg criada com sucesso!")

# Criar 3 empresas exemplo baseadas nas empresas_verdes existentes
cursor.execute("SELECT cnpj, razao_social, nome_fantasia, municipio, uf FROM empresas_verdes LIMIT 3")
empresas = cursor.fetchall()

empresas_teste = []
for i, emp in enumerate(empresas, 1):
    cnpj, razao, fantasia, cidade, uf = emp
    email = f"contato{i}@{razao[:10].lower().replace(' ', '')}.com.br"
    senha_hash = hashlib.sha256(f"senha123".encode()).hexdigest()
    
    cursor.execute("""
        INSERT OR IGNORE INTO empresas_esg 
        (cnpj, razao_social, nome_fantasia, email, senha_hash, cidade, estado, setor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cnpj, razao, fantasia or razao, email, senha_hash, cidade, uf, 'Sustentabilidade', 'ativa'))
    
    empresas_teste.append({
        'email': email,
        'senha': 'senha123',
        'razao_social': razao
    })

conn.commit()

print(f"\n✅ {len(empresas_teste)} empresas de teste criadas!")
print("\n📋 CREDENCIAIS DE LOGIN:")
print("="*60)
for emp in empresas_teste:
    print(f"\n🏢 {emp['razao_social']}")
    print(f"   Email: {emp['email']}")
    print(f"   Senha: {emp['senha']}")

# Vincular vagas às empresas (atualizar CNPJ nas vagas)
cursor.execute("SELECT id, cnpj FROM empresas_esg")
empresas_ids = cursor.fetchall()

vagas_atualizadas = 0
for emp_id, cnpj in empresas_ids:
    # Buscar vagas sem empresa (limitado a 10 por empresa)
    cursor.execute("""
        SELECT id FROM vagas_esg 
        WHERE cnpj IS NULL OR cnpj='' 
        LIMIT 10
    """)
    vagas_sem_empresa = cursor.fetchall()
    
    for (vaga_id,) in vagas_sem_empresa:
        cursor.execute("UPDATE vagas_esg SET cnpj=? WHERE id=?", (cnpj, vaga_id))
        vagas_atualizadas += 1

conn.commit()
print(f"\n✅ {vagas_atualizadas} vagas vinculadas às empresas")

# Estatísticas
cursor.execute("SELECT COUNT(*) FROM empresas_esg")
total_empresas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM vagas_esg WHERE cnpj IS NOT NULL")
vagas_vinculadas = cursor.fetchone()[0]

print("\n" + "="*60)
print("📊 ESTATÍSTICAS:")
print(f"   • {total_empresas} empresas cadastradas")
print(f"   • {vagas_vinculadas} vagas vinculadas a empresas")
print("="*60)

conn.close()
