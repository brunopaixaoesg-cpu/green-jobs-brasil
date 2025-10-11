"""
Script para executar migration 002: Profissionais ESG
"""

import sqlite3
import os

# Caminho do banco de dados
DB_PATH = "gjb_dev.db"
MIGRATION_FILE = "db/migrations/002_create_profissionais_esg.sql"

def run_migration():
    """Executa a migration 002"""
    
    # Verificar se arquivo existe
    if not os.path.exists(MIGRATION_FILE):
        print(f"❌ Arquivo de migration não encontrado: {MIGRATION_FILE}")
        return False
    
    # Ler migration
    with open(MIGRATION_FILE, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    # Conectar ao banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Executar migration
        cursor.executescript(migration_sql)
        conn.commit()
        
        # Verificar resultados
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        total_prof = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM experiencias_profissionais")
        total_exp = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM formacoes_academicas")
        total_form = cursor.fetchone()[0]
        
        print("✅ Migration 002 executada com sucesso!")
        print(f"   - Tabela profissionais_esg criada com {total_prof} registros")
        print(f"   - Tabela experiencias_profissionais criada com {total_exp} registros")
        print(f"   - Tabela formacoes_academicas criada com {total_form} registros")
        
        # Mostrar alguns exemplos
        print("\n📊 Profissionais cadastrados:")
        cursor.execute("""
            SELECT nome_completo, cargo_atual, anos_experiencia_esg, nivel_desejado 
            FROM profissionais_esg 
            ORDER BY anos_experiencia_esg DESC
        """)
        
        for row in cursor.fetchall():
            print(f"   • {row[0]} - {row[1]} ({row[2]} anos ESG) - Nível {row[3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar migration: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Executando Migration 002: Sistema de Profissionais ESG\n")
    success = run_migration()
    
    if success:
        print("\n✅ Sistema de profissionais pronto para uso!")
    else:
        print("\n❌ Falha na execução da migration")
