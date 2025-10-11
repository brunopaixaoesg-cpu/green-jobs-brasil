"""
Setup do banco PostgreSQL usando Python e SQLAlchemy
"""
import os
import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import psycopg2
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError as e:
    logger.error(f"Dependência não encontrada: {e}")
    logger.info("Execute: pip install psycopg2-binary sqlalchemy python-dotenv")
    sys.exit(1)

# Carregar variáveis de ambiente
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/gjb_db")
logger.info(f"Usando DATABASE_URL: {DATABASE_URL.replace(':123456', ':****')}")

def create_database():
    """Criar o banco de dados se não existir."""
    try:
        # Conectar ao postgres padrão para criar o banco
        base_url = DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
        engine = create_engine(base_url)
        
        with engine.connect() as conn:
            # Usar autocommit para CREATE DATABASE
            conn.execute(text("COMMIT"))
            try:
                conn.execute(text("CREATE DATABASE gjb_db"))
                logger.info("✅ Banco gjb_db criado com sucesso!")
            except Exception as e:
                if "already exists" in str(e).lower():
                    logger.info("ℹ️  Banco gjb_db já existe")
                else:
                    logger.warning(f"Aviso ao criar banco: {e}")
        
        engine.dispose()
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar banco: {e}")
        return False

def apply_schema():
    """Aplicar o schema do banco."""
    try:
        engine = create_engine(DATABASE_URL)
        
        # Ler arquivo schema.sql
        schema_path = Path("db/schema.sql")
        if not schema_path.exists():
            logger.error("❌ Arquivo db/schema.sql não encontrado")
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Executar schema
        with engine.connect() as conn:
            # Dividir em comandos individuais
            commands = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip()]
            
            for cmd in commands:
                if cmd:
                    try:
                        conn.execute(text(cmd))
                        conn.commit()
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            logger.warning(f"Aviso no comando: {e}")
        
        logger.info("✅ Schema aplicado com sucesso!")
        engine.dispose()
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao aplicar schema: {e}")
        return False

def load_seed_data():
    """Carregar dados seed dos CNAEs."""
    try:
        engine = create_engine(DATABASE_URL)
        
        # Primeiro, verificar se tabela cnae_green existe e tem dados
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM gjb.cnae_green")).scalar()
            if result > 0:
                logger.info(f"ℹ️  Tabela cnae_green já tem {result} registros")
                return True
        
        # Ler dados do CSV e inserir manualmente
        import pandas as pd
        
        csv_path = Path("etl/cnae_green_seed.csv")
        if not csv_path.exists():
            logger.error("❌ Arquivo etl/cnae_green_seed.csv não encontrado")
            return False
        
        df = pd.read_csv(csv_path)
        logger.info(f"Carregando {len(df)} registros de CNAEs verdes...")
        
        with engine.connect() as conn:
            for _, row in df.iterrows():
                conn.execute(text("""
                    INSERT INTO gjb.cnae_green (cnae, titulo, categoria, ods_raw, prioridade, observacoes)
                    VALUES (:cnae, :titulo, :categoria, :ods_raw, :prioridade, :observacoes)
                    ON CONFLICT (cnae) DO NOTHING
                """), {
                    'cnae': row['cnae'],
                    'titulo': row['titulo'],
                    'categoria': row['categoria'],
                    'ods_raw': row.get('ods_raw', ''),
                    'prioridade': row['prioridade'],
                    'observacoes': row.get('observacoes', '')
                })
            conn.commit()
        
        logger.info("✅ Dados seed carregados com sucesso!")
        engine.dispose()
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados seed: {e}")
        return False

def test_connection():
    """Testar conexão com o banco."""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                logger.info("✅ Conexão com banco testada com sucesso!")
                return True
        engine.dispose()
        return False
    except Exception as e:
        logger.error(f"❌ Erro na conexão: {e}")
        return False

def main():
    """Função principal."""
    logger.info("🚀 Iniciando setup do banco PostgreSQL...")
    
    # Passo 1: Criar banco
    if not create_database():
        logger.error("Falha ao criar banco. Verifique credenciais e tente novamente.")
        return False
    
    # Passo 2: Testar conexão
    if not test_connection():
        logger.error("Falha na conexão. Verifique URL e credenciais.")
        return False
    
    # Passo 3: Aplicar schema
    if not apply_schema():
        logger.error("Falha ao aplicar schema.")
        return False
    
    # Passo 4: Carregar dados seed
    if not load_seed_data():
        logger.error("Falha ao carregar dados seed.")
        return False
    
    logger.info("🎉 Setup do banco concluído com sucesso!")
    logger.info("Próximo passo: execute 'python etl/main.py' para processar dados")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)