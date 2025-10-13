import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("=== EMPRESAS NO BANCO ===")
cursor.execute("SELECT cnpj, razao_social FROM empresas_verdes LIMIT 10")
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]}")

print("\n=== CNPJ DA VAGA ===")
cursor.execute("SELECT id, cnpj, titulo FROM vagas_esg")
for row in cursor.fetchall():
    print(f"Vaga {row[0]}: CNPJ={row[1]} | {row[2]}")

conn.close()
