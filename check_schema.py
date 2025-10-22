"""Script para verificar schema do banco de dados"""
import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Verificar tabelas de empresa
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%empresa%'")
empresas_tables = cursor.fetchall()
print("📊 Tabelas relacionadas a empresa:", empresas_tables if empresas_tables else "Nenhuma encontrada")

# Verificar estrutura de vagas
print("\n📋 Estrutura da tabela vagas_esg:")
cursor.execute("PRAGMA table_info(vagas_esg)")
cols = cursor.fetchall()
for col in cols:
    print(f"  • {col[1]} ({col[2]})")

# Verificar se vagas têm empresa_id
has_empresa_id = any(col[1] == 'empresa_id' for col in cols)
print(f"\n✓ Campo empresa_id existe: {has_empresa_id}")

# Contar vagas
cursor.execute("SELECT COUNT(*) FROM vagas_esg")
total_vagas = cursor.fetchone()[0]
print(f"\n📈 Total de vagas no banco: {total_vagas}")

conn.close()
