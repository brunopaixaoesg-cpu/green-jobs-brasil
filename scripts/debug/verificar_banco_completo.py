import sqlite3
import os

# Verificar se o banco existe
db_path = 'api/gjb_dev.db'
print(f"🔍 Verificando banco: {db_path}")
print(f"📁 Arquivo existe: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    print(f"📏 Tamanho do arquivo: {os.path.getsize(db_path)} bytes")

try:
    from scripts.db_wrapper import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
    
    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"📋 Tabelas encontradas: {[t[0] for t in tables]}")
    
    # Verificar dados em cada tabela
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"📊 {table_name}: {count} registros")
        
        # Se há registros, mostrar alguns dados
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print(f"   Exemplos: {rows}")
    
    # connection closed by context manager
    
except Exception as e:
    print(f"❌ Erro: {e}")