"""Script para verificar a estrutura das tabelas"""
import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
c = conn.cursor()

print('=== ESTRUTURA DA TABELA profissionais_esg ===')
c.execute("PRAGMA table_info(profissionais_esg)")
for col in c.fetchall():
    print(f"  {col[1]} ({col[2]})")

print('\n=== ESTRUTURA DA TABELA candidaturas_esg ===')
c.execute("PRAGMA table_info(candidaturas_esg)")
for col in c.fetchall():
    print(f"  {col[1]} ({col[2]})")

print('\n=== DADOS DE EXEMPLO profissionais_esg ===')
c.execute("SELECT * FROM profissionais_esg LIMIT 1")
row = c.fetchone()
if row:
    c.execute("PRAGMA table_info(profissionais_esg)")
    cols = [col[1] for col in c.fetchall()]
    for col, val in zip(cols, row):
        print(f"  {col}: {val}")

conn.close()
