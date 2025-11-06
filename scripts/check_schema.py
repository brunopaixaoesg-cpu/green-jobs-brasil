import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
cursor = conn.cursor()

# Profissionais
cursor.execute("PRAGMA table_info(profissionais_esg)")
print("=== profissionais_esg ===")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

print("\n=== empresas_esg ===")
cursor.execute("PRAGMA table_info(empresas_esg)")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

print("\n=== vagas ===")
cursor.execute("PRAGMA table_info(vagas)")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

print("\n=== candidaturas ===")
cursor.execute("PRAGMA table_info(candidaturas)")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

conn.close()
