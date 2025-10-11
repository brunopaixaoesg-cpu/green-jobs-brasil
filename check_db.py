import sqlite3

# Conectar ao banco
conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tabelas no banco:")
for table in tables:
    print(f"- {table[0]}")

# Verificar cada tabela
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT count(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"\nTabela {table_name}: {count} registros")
    
    # Mostrar estrutura
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Colunas:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()