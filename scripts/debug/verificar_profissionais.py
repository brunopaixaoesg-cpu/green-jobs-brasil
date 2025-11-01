from scripts.db_wrapper import get_connection

with get_connection() as conn:
    cursor = conn.cursor()

# Procurar tabelas relacionadas a profissionais
cursor.execute("SELECT name FROM sqlite_master WHERE name LIKE '%profission%'")
tables = cursor.fetchall()
print('Tabelas relacionadas a profissionais:')
for table in tables:
    print(f'  {table[0]}')

# Verificar se existe tabela profissionais
cursor.execute("SELECT name FROM sqlite_master WHERE name = 'profissionais'")
table_exists = cursor.fetchone()
if table_exists:
    print('\nTabela "profissionais" existe!')
    cursor.execute("SELECT COUNT(*) FROM profissionais")
    count = cursor.fetchone()[0]
    print(f'Registros na tabela profissionais: {count}')
    
    if count > 0:
        cursor.execute("SELECT * FROM profissionais LIMIT 1")
        sample = cursor.fetchone()
        cursor.execute("PRAGMA table_info(profissionais)")
        columns = cursor.fetchall()
        print('\nSchema da tabela profissionais:')
        for i, col in enumerate(columns):
            value = sample[i] if sample and i < len(sample) else 'NULL'
            print(f'  {col[1]} ({col[2]}): {value}')
else:
    print('\nTabela "profissionais" NÃO existe!')

# connection closed by context manager