import sqlite3
import os

# Verificar se o banco existe
banco_path = 'api/gjb_dev.db'
print("=== VERIFICAÇÃO DO BANCO DE DADOS ===")
print(f"Banco existe: {os.path.exists(banco_path)}")

if not os.path.exists(banco_path):
    print("❌ Banco não encontrado! Será criado automaticamente na próxima inicialização da API.")
    exit()

# Verificar dados no banco
from scripts.db_wrapper import get_connection
with get_connection() as conn:
    cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tabelas = cursor.fetchall()
print(f"\nTabelas existentes: {len(tabelas)}")
for tabela in tabelas:
    print(f"  - {tabela[0]}")

if 'empresas_esg' in [t[0] for t in tabelas]:
    # Verificar empresas
    cursor.execute('SELECT COUNT(*) FROM empresas_esg')
    total_empresas = cursor.fetchone()[0]
    print(f"\nTotal empresas: {total_empresas}")

    if total_empresas > 0:
        cursor.execute('SELECT id, razao_social, cnpj FROM empresas_esg LIMIT 3')
        print("Empresas:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Nome: {row[1]}, CNPJ: {row[2]}")

if 'vagas' in [t[0] for t in tabelas]:
    # Verificar vagas
    cursor.execute('SELECT COUNT(*) FROM vagas')
    total_vagas = cursor.fetchone()[0]
    print(f"\nTotal vagas: {total_vagas}")

    if total_vagas > 0:
        cursor.execute('SELECT id, titulo, empresa_id, ativa FROM vagas LIMIT 3')
        print("Vagas:")
        for row in cursor.fetchall():
            print(f"  ID: {row[0]}, Título: {row[1]}, Empresa ID: {row[2]}, Ativa: {row[3]}")

# connection closed by context manager
print("\n=== FIM DA VERIFICAÇÃO ===")