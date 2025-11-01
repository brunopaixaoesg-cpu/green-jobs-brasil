"""Script para verificar o conteúdo do banco de dados"""
import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
c = conn.cursor()

print('=== TABELAS NO BANCO ===')
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
for table in tables:
    print(f"  - {table}")

print('\n=== CONTAGENS POR TABELA ===')
for table in ['empresas_esg', 'profissionais_esg', 'vagas', 'candidaturas_esg']:
    try:
        c.execute(f'SELECT COUNT(*) FROM {table}')
        count = c.fetchone()[0]
        print(f'{table}: {count} registros')
    except Exception as e:
        print(f'{table}: ERRO - {e}')

conn.close()
