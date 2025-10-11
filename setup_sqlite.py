"""
Setup do banco SQLite - Versão Simplificada
"""
import sqlite3
import pandas as pd
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_sqlite_db():
    """Configurar banco SQLite completo."""
    try:
        # Conectar ao SQLite
        conn = sqlite3.connect('gjb_dev.db')
        cursor = conn.cursor()
        
        logger.info("🗄️  Criando schema SQLite...")
        
        # Aplicar schema
        with open('db/schema_sqlite.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cursor.executescript(schema_sql)
        
        logger.info("📊 Carregando dados CNAEs...")
        
        # Carregar CNAEs
        df_cnaes = pd.read_csv('etl/cnae_green_seed.csv')
        
        for _, row in df_cnaes.iterrows():
            # Processar ODS tags
            ods_raw = str(row.get('ods_raw', ''))
            ods_tags = []
            if ods_raw and ods_raw != 'nan':
                try:
                    ods_tags = [int(x.strip()) for x in ods_raw.split(',') if x.strip().isdigit()]
                except:
                    pass
            
            cursor.execute("""
                INSERT OR REPLACE INTO cnae_green 
                (cnae, titulo, categoria, ods_raw, ods_tags, prioridade, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row['cnae'],
                row['titulo'],
                row['categoria'],
                ods_raw,
                json.dumps(ods_tags),
                row['prioridade'],
                row.get('observacoes', '')
            ))
        
        conn.commit()
        
        # Verificar dados
        cursor.execute("SELECT COUNT(*) FROM cnae_green")
        count = cursor.fetchone()[0]
        logger.info(f"✅ {count} CNAEs carregados com sucesso!")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no setup: {e}")
        return False

if __name__ == "__main__":
    if setup_sqlite_db():
        logger.info("🎉 Banco SQLite configurado com sucesso!")
        logger.info("Próximo passo: execute o ETL")
    else:
        logger.error("❌ Falha no setup do banco")