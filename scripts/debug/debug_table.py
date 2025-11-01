import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("=== ESTRUTURA empresas_esg ===")
cursor.execute("PRAGMA table_info(empresas_esg)")
cols = cursor.fetchall()
for col in cols:
    print(f"  • {col[1]} ({col[2]})")

print("\n=== CONTEÚDO empresas_esg ===")
cursor.execute("SELECT * FROM empresas_esg LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(f"  {row}")

conn.close()