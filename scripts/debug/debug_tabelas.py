import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Verificar todas as tabelas que contêm dados de pessoas
all_tables = [
    'profissionais',
    'profissionais_esg', 
    'users'
]

for table in all_tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f'{table}: {count} registros')
        
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            sample = cursor.fetchone()
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f'  Exemplo de registro em {table}:')
            for i, col in enumerate(columns):
                value = sample[i] if sample and i < len(sample) else 'NULL'
                print(f'    {col[1]}: {value}')
            print()
    except Exception as e:
        print(f'{table}: Tabela não existe ou erro - {e}')

conn.close()