"""
Script para executar migrations no banco de dados
"""
import sqlite3
import os
from pathlib import Path

def run_migration(db_path, migration_file):
    """Executa uma migration SQL no banco de dados"""
    print(f"\n🔄 Executando migration: {migration_file}")
    
    # Ler arquivo SQL
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Executar SQL
        cursor.executescript(sql)
        conn.commit()
        print(f"✅ Migration executada com sucesso!")
        
        # Verificar tabelas criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📊 Tabelas no banco: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ Erro ao executar migration: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    # Caminhos
    project_root = Path(__file__).parent
    db_path = project_root / "gjb_dev.db"
    migrations_dir = project_root / "db" / "migrations"
    
    print("🚀 Green Jobs Brasil - Migration Runner")
    print("=" * 50)
    print(f"📂 Banco de dados: {db_path}")
    print(f"📁 Diretório migrations: {migrations_dir}")
    
    # Verificar se banco existe
    if not db_path.exists():
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return
    
    # Listar migrations
    migrations = sorted(migrations_dir.glob("*.sql"))
    
    if not migrations:
        print("⚠️ Nenhuma migration encontrada!")
        return
    
    print(f"\n📋 Migrations encontradas: {len(migrations)}")
    for mig in migrations:
        print(f"  - {mig.name}")
    
    # Executar migrations
    for migration_file in migrations:
        run_migration(db_path, migration_file)
    
    print("\n✅ Todas as migrations foram executadas!")
    print("=" * 50)

if __name__ == "__main__":
    main()
