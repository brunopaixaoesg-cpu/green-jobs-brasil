import sqlite3
conn = sqlite3.connect('api/gjb_dev.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT id, nome, email FROM profissionais_esg LIMIT 5')
for r in cursor.fetchall():
    print(f'ID {r["id"]}: {r["nome"]} ({r["email"]})')
conn.close()
