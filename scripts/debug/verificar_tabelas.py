import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tabelas no banco:')
for table in tables:
    print(f'  {table[0]}')

# Verificar contagem de registros em cada tabela
for table in tables:
    table_name = table[0]
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f'  {table_name}: {count} registros')
    except Exception as e:
        print(f'  {table_name}: Erro - {e}')

conn.close()