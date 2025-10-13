import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Verificar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("=== TABELAS NO BANCO ===")
for table in tables:
    print(f"  - {table[0]}")

# Verificar se vagas_esg existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vagas_esg'")
vaga_table = cursor.fetchone()

if vaga_table:
    print("\n✅ Tabela vagas_esg EXISTE")
    
    # Contar vagas
    cursor.execute("SELECT COUNT(*) FROM vagas_esg")
    total = cursor.fetchone()[0]
    print(f"   Total de vagas: {total}")
    
    if total > 0:
        cursor.execute("SELECT id, titulo, status FROM vagas_esg LIMIT 3")
        vagas = cursor.fetchall()
        print("\n   Primeiras vagas:")
        for v in vagas:
            print(f"   - ID {v[0]}: {v[1]} ({v[2]})")
else:
    print("\n❌ Tabela vagas_esg NÃO EXISTE")
    print("\nExecute a migration 001:")
    print("python run_migration_001.py")

conn.close()
