"""Listar todas as tabelas do banco"""
import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📊 Tabelas no banco gjb_dev.db:\n")
for table in tables:
    print(f"  - {table[0]}")
    
conn.close()
