"""Verificar tabelas do banco de dados"""
import sqlite3
import sys
import os

# Adicionar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from api.db import get_db

conn = get_db()
cursor = conn.cursor()

print("="*50)
print("TABELAS NO BANCO DE DADOS")
print("="*50)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"\n📋 {table_name}")
    
    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"   Registros: {count}")
    
    # Mostrar estrutura
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"   Colunas: {len(columns)}")
    
conn.close()

print("\n" + "="*50)
print("FIM")
print("="*50)
