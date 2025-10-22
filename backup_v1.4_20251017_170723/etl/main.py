"""
Green Jobs Brasil - ETL Main Pipeline
Processes RFB CNPJ datasets to identify and classify green companies.
"""

import logging
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas as pd
import duckdb
import psycopg2
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, date

from config import config, ScoringRules

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GreenJobsETL:
    """Main ETL pipeline for Green Jobs Brasil."""
    
    def __init__(self):
        self.duckdb_conn = None
        self.postgres_conn = None
        self.cnae_green_mapping = {}
        self.cnae_priorities = {}
        
    def __enter__(self):
        """Context manager entry."""
        try:
            # Initialize DuckDB connection
            self.duckdb_conn = duckdb.connect(':memory:')
            logger.info("DuckDB connection established")
            
            # Initialize SQLite connection
            import sqlite3
            self.postgres_conn = sqlite3.connect('gjb_dev.db')
            logger.info("SQLite connection established")
            
            return self
            
        except Exception as e:
            logger.error(f"Failed to establish database connections: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.duckdb_conn:
            self.duckdb_conn.close()
        if self.postgres_conn:
            self.postgres_conn.close()
        logger.info("Database connections closed")
    
    def load_cnae_green_mapping(self) -> None:
        """Load CNAE green classification mapping from seed file."""
        try:
            df = pd.read_csv(config.CNAE_GREEN_SEED)
            
            for _, row in df.iterrows():
                cnae = row['cnae']
                self.cnae_green_mapping[cnae] = {
                    'titulo': row['titulo'],
                    'categoria': row['categoria'],
                    'ods_raw': row.get('ods_raw', ''),
                    'prioridade': row['prioridade']
                }
                self.cnae_priorities[cnae] = row['prioridade']
            
            logger.info(f"Loaded {len(self.cnae_green_mapping)} green CNAEs")
            
        except Exception as e:
            logger.error(f"Failed to load CNAE green mapping: {e}")
            raise
    
    def setup_duckdb_schema(self) -> None:
        """Create DuckDB tables for data processing."""
        try:
            # Create empresas table
            self.duckdb_conn.execute("""
                CREATE TABLE empresas (
                    cnpj VARCHAR,
                    razao_social VARCHAR,
                    natureza_juridica VARCHAR,
                    qualificacao_responsavel VARCHAR,
                    capital_social DECIMAL,
                    porte VARCHAR,
                    ente_federativo_responsavel VARCHAR
                )
            """)
            
            # Create estabelecimentos table
            self.duckdb_conn.execute("""
                CREATE TABLE estabelecimentos (
                    cnpj VARCHAR,
                    cnpj_ordem VARCHAR,
                    cnpj_dv VARCHAR,
                    identificador_matriz_filial VARCHAR,
                    nome_fantasia VARCHAR,
                    situacao_cadastral VARCHAR,
                    data_situacao_cadastral DATE,
                    motivo_situacao_cadastral VARCHAR,
                    nome_cidade_exterior VARCHAR,
                    pais VARCHAR,
                    data_inicio_atividade DATE,
                    cnae_fiscal_principal VARCHAR,
                    cnae_fiscal_secundaria VARCHAR,
                    tipo_logradouro VARCHAR,
                    logradouro VARCHAR,
                    numero VARCHAR,
                    complemento VARCHAR,
                    bairro VARCHAR,
                    cep VARCHAR,
                    uf VARCHAR,
                    municipio VARCHAR,
                    ddd1 VARCHAR,
                    telefone1 VARCHAR,
                    ddd2 VARCHAR,
                    telefone2 VARCHAR,
                    ddd_fax VARCHAR,
                    fax VARCHAR,
                    correio_eletronico VARCHAR,
                    situacao_especial VARCHAR,
                    data_situacao_especial DATE
                )
            """)
            
            logger.info("DuckDB schema created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create DuckDB schema: {e}")
            raise
    
    def load_rfb_data(self) -> None:
        """Load RFB datasets into DuckDB."""
        try:
            # Load empresas data
            empresas_files = list(config.RAW_DIR.glob(config.CNPJ_FILE))
            if not empresas_files:
                logger.warning(f"No empresas files found matching {config.CNPJ_FILE}")
                # Create sample data for testing
                self._create_sample_empresas_data()
            else:
                for file_path in empresas_files:
                    logger.info(f"Loading empresas data from {file_path}")
                    self.duckdb_conn.execute(f"""
                        INSERT INTO empresas 
                        SELECT * FROM read_csv_auto('{file_path}', header=true, delimiter=';')
                    """)
            
            # Load estabelecimentos data
            estab_files = list(config.RAW_DIR.glob(config.ESTABELECIMENTOS_FILE))
            if not estab_files:
                logger.warning(f"No estabelecimentos files found matching {config.ESTABELECIMENTOS_FILE}")
                # Create sample data for testing
                self._create_sample_estabelecimentos_data()
            else:
                for file_path in estab_files:
                    logger.info(f"Loading estabelecimentos data from {file_path}")
                    self.duckdb_conn.execute(f"""
                        INSERT INTO estabelecimentos 
                        SELECT * FROM read_csv_auto('{file_path}', header=true, delimiter=';')
                    """)
            
            # Log data counts
            empresas_count = self.duckdb_conn.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
            estab_count = self.duckdb_conn.execute("SELECT COUNT(*) FROM estabelecimentos").fetchone()[0]
            
            logger.info(f"Loaded {empresas_count} empresas and {estab_count} estabelecimentos")
            
        except Exception as e:
            logger.error(f"Failed to load RFB data: {e}")
            raise
    
    def _create_sample_empresas_data(self) -> None:
        """Create sample empresas data for testing."""
        sample_data = [
            ("12345678000195", "Solar Energy Brasil Ltda", "206", "05", 1000000.00, "03", ""),
            ("98765432000123", "Reciclagem Verde SA", "205", "05", 500000.00, "02", ""),
            ("11223344000167", "Tratamento de Água Limpa", "206", "05", 2000000.00, "03", ""),
            ("55667788000145", "Energia Eólica do Norte", "205", "05", 5000000.00, "04", ""),
            ("99887766000134", "Consultoria Sustentável", "206", "05", 100000.00, "01", ""),
            ("88776655000178", "Biomassa Energia Verde", "205", "05", 3000000.00, "04", ""),
            ("77665544000189", "Coleta Seletiva MG", "206", "05", 800000.00, "02", ""),
            ("66554433000190", "Hidrelétrica Sustentável", "205", "05", 10000000.00, "04", ""),
            ("55443322000101", "Gestão Resíduos SP", "206", "05", 1500000.00, "03", ""),
            ("44332211000112", "Energia Solar RJ", "205", "05", 2500000.00, "03", ""),
        ]
        
        for data in sample_data:
            self.duckdb_conn.execute("""
                INSERT INTO empresas VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
        
        logger.info("Created sample empresas data")
    
    def _create_sample_estabelecimentos_data(self) -> None:
        """Create sample estabelecimentos data for testing."""
        # Usar apenas os campos necessários para o schema DuckDB
        estabelecimentos_data = [
            ("12345678000195", "0001", "95", "1", "Solar Energy Brasil", "02", "2020-01-15", "00", "", "", "2020-01-15", "3511-5/02", "3511-5/01,3512-3/01", "RUA", "Das Energias", "100", "", "Centro", "30000000", "MG", "Belo Horizonte", "", "", "", "", "", "", "", ""),
            ("98765432000123", "0001", "23", "1", "Reciclagem Verde", "02", "2019-05-20", "00", "", "", "2019-05-20", "3831-9/00", "3832-7/00", "AV", "Sustentável", "200", "", "Industrial", "20000000", "RJ", "Rio de Janeiro", "", "", "", "", "", "", "", ""),
            ("11223344000167", "0001", "67", "1", "Água Limpa", "02", "2018-03-10", "00", "", "", "2018-03-10", "3600-6/01", "", "RUA", "Das Águas", "300", "", "Saneamento", "01000000", "SP", "São Paulo", "", "", "", "", "", "", "", ""),
            ("55667788000145", "0001", "45", "1", "Eólica Norte", "02", "2021-07-01", "00", "", "", "2021-07-01", "3511-5/03", "", "EST", "dos Ventos", "400", "", "Energia", "40000000", "RJ", "Niterói", "", "", "", "", "", "", "", ""),
            ("99887766000134", "0001", "34", "1", "Consultoria Verde", "02", "2022-02-28", "00", "", "", "2022-02-28", "7490-1/04", "", "RUA", "Consultores", "500", "", "Comercial", "30000000", "MG", "Uberlândia", "", "", "", "", "", "", "", ""),
            ("88776655000178", "0001", "78", "1", "Biomassa Energia", "02", "2020-08-15", "00", "", "", "2020-08-15", "3511-5/04", "3600-6/01", "AV", "Biomassa", "600", "", "Industrial", "35000000", "MG", "Juiz de Fora", "", "", "", "", "", "", "", ""),
            ("77665544000189", "0001", "89", "1", "Coleta Seletiva", "02", "2021-03-20", "00", "", "", "2021-03-20", "3811-4/00", "3831-9/00", "RUA", "Reciclagem", "700", "", "Centro", "31000000", "MG", "Contagem", "", "", "", "", "", "", "", ""),
            ("66554433000190", "0001", "90", "1", "Hidrelétrica Verde", "02", "2019-11-10", "00", "", "", "2019-11-10", "3511-5/01", "", "EST", "Energia", "800", "", "Rural", "22000000", "RJ", "Teresópolis", "", "", "", "", "", "", "", ""),
            ("55443322000101", "0001", "01", "1", "Gestão Resíduos", "02", "2020-05-25", "00", "", "", "2020-05-25", "3821-1/00", "3822-0/00", "AV", "Limpeza", "900", "", "Industrial", "05000000", "SP", "Guarulhos", "", "", "", "", "", "", "", ""),
            ("44332211000112", "0001", "12", "1", "Solar RJ", "02", "2021-09-30", "00", "", "", "2021-09-30", "3511-5/02", "3513-1/01", "RUA", "Solar", "1000", "", "Tecnológico", "21000000", "RJ", "Rio de Janeiro", "", "", "", "", "", "", "", ""),
        ]
        
        for data in estabelecimentos_data:
            self.duckdb_conn.execute("""
                INSERT INTO estabelecimentos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        
        logger.info("Created sample estabelecimentos data")
    
    def process_green_companies(self) -> pd.DataFrame:
        """Process and identify green companies."""
        try:
            # Create view with joined data filtered by green CNAEs and target UFs
            green_cnaes = list(self.cnae_green_mapping.keys())
            green_cnaes_str = "','".join(green_cnaes)
            target_ufs_str = "','".join(config.TARGET_UFS)
            
            self.duckdb_conn.execute(f"""
                CREATE VIEW green_companies AS
                SELECT 
                    e.cnpj,
                    e.razao_social,
                    est.nome_fantasia,
                    est.cnae_fiscal_principal as cnae_principal,
                    CASE 
                        WHEN est.cnae_fiscal_secundaria IS NOT NULL AND est.cnae_fiscal_secundaria != ''
                        THEN string_split(est.cnae_fiscal_secundaria, ',')
                        ELSE []
                    END as cnaes_secundarias,
                    e.porte,
                    est.uf,
                    est.municipio,
                    est.situacao_cadastral,
                    est.data_inicio_atividade as data_abertura
                FROM empresas e
                JOIN estabelecimentos est ON e.cnpj = est.cnpj
                WHERE (est.cnae_fiscal_principal IN ('{green_cnaes_str}')
                       OR EXISTS (
                           SELECT 1 FROM unnest(string_split(est.cnae_fiscal_secundaria, ',')) as sec_cnae
                           WHERE sec_cnae IN ('{green_cnaes_str}')
                       ))
                  AND est.uf IN ('{target_ufs_str}')
                  AND est.identificador_matriz_filial = '1'
            """)
            
            # Fetch processed data
            df = self.duckdb_conn.execute("SELECT * FROM green_companies").df()
            
            if df.empty:
                logger.warning("No green companies found in the data")
                return df
            
            # Calculate green scores and ODS tags
            df['score_verde'] = df.apply(
                lambda row: ScoringRules.calculate_score(
                    row['cnae_principal'],
                    row['cnaes_secundarias'] if row['cnaes_secundarias'] else [],
                    row['situacao_cadastral'],
                    self.cnae_priorities
                ), axis=1
            )
            
            # Calculate ODS tags
            df['ods_tags'] = df.apply(self._calculate_ods_tags, axis=1)
            
            # Add metadata
            df['fonte_atualizacao'] = 'ETL_RFB'
            df['atualizado_em'] = datetime.now()
            
            logger.info(f"Processed {len(df)} green companies")
            return df
            
        except Exception as e:
            logger.error(f"Failed to process green companies: {e}")
            raise
    
    def _calculate_ods_tags(self, row) -> List[int]:
        """Calculate ODS tags for a company based on its CNAEs."""
        ods_tags = set()
        
        # Add ODS from primary CNAE
        if row['cnae_principal'] in self.cnae_green_mapping:
            ods_raw = self.cnae_green_mapping[row['cnae_principal']].get('ods_raw', '')
            if ods_raw:
                ods_tags.update(self._parse_ods_string(ods_raw))
        
        # Add ODS from secondary CNAEs
        for cnae in row['cnaes_secundarias'] if row['cnaes_secundarias'] else []:
            cnae = cnae.strip()
            if cnae in self.cnae_green_mapping:
                ods_raw = self.cnae_green_mapping[cnae].get('ods_raw', '')
                if ods_raw:
                    ods_tags.update(self._parse_ods_string(ods_raw))
        
        return sorted(list(ods_tags))
    
    def _parse_ods_string(self, ods_raw: str) -> Set[int]:
        """Parse ODS string into set of integers."""
        if not ods_raw:
            return set()
        
        try:
            return set(int(x.strip()) for x in ods_raw.split(',') if x.strip().isdigit())
        except:
            return set()
    
    def save_to_parquet(self, df: pd.DataFrame) -> None:
        """Save processed data to partitioned Parquet files."""
        try:
            config.ensure_directories()
            
            # Convert to PyArrow table
            table = pa.Table.from_pandas(df)
            
            # Write partitioned by UF
            output_path = config.PROCESSED_DIR / "empresas_verdes"
            output_path.mkdir(exist_ok=True)
            
            pq.write_to_dataset(
                table,
                root_path=str(output_path),
                partition_cols=['uf'],
                compression='snappy',
                existing_data_behavior='overwrite_or_ignore'
            )
            
            logger.info(f"Saved Parquet data to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save Parquet data: {e}")
            raise
    
    def load_to_postgres(self, df: pd.DataFrame) -> None:
        """Load processed data to SQLite."""
        try:
            cursor = self.postgres_conn.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM empresas_verdes")
            cursor.execute("DELETE FROM empresa_cnae")
            
            # Insert empresas_verdes data
            for _, row in df.iterrows():
                # Convert arrays to JSON strings for SQLite
                cnaes_secundarias_json = json.dumps(row['cnaes_secundarias'] if row['cnaes_secundarias'] else [])
                ods_tags_json = json.dumps(row['ods_tags'] if row['ods_tags'] else [])
                
                cursor.execute("""
                    INSERT INTO empresas_verdes 
                    (cnpj, razao_social, nome_fantasia, cnae_principal, cnaes_secundarias,
                     porte, uf, municipio, situacao_cadastral, data_abertura, score_verde,
                     ods_tags, fonte_atualizacao, atualizado_em)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['cnpj'], row['razao_social'], row['nome_fantasia'],
                    row['cnae_principal'], cnaes_secundarias_json, row['porte'],
                    row['uf'], row['municipio'], row['situacao_cadastral'],
                    row['data_abertura'], row['score_verde'], ods_tags_json,
                    row['fonte_atualizacao'], row['atualizado_em']
                ))
                
                # Insert empresa_cnae relationships
                # Primary CNAE
                cursor.execute("""
                    INSERT OR IGNORE INTO empresa_cnae (cnpj, codigo_cnae)
                    VALUES (?, ?)
                """, (row['cnpj'], row['cnae_principal']))
                
                # Secondary CNAEs
                for cnae in row['cnaes_secundarias'] if row['cnaes_secundarias'] else []:
                    cnae = cnae.strip()
                    if cnae and cnae in self.cnae_green_mapping:
                        cursor.execute("""
                            INSERT OR IGNORE INTO empresa_cnae (cnpj, codigo_cnae)
                            VALUES (?, ?)
                        """, (row['cnpj'], cnae))
            
            # Commit changes
            self.postgres_conn.commit()
            
            logger.info(f"Loaded {len(df)} companies to SQLite")
            
        except Exception as e:
            logger.error(f"Failed to load data to SQLite: {e}")
            if self.postgres_conn:
                self.postgres_conn.rollback()
            raise
    
    def run_pipeline(self) -> None:
        """Execute the complete ETL pipeline."""
        start_time = time.time()
        
        try:
            logger.info("Starting Green Jobs Brasil ETL pipeline")
            
            # Validate configuration
            if not config.validate_config():
                raise ValueError("Invalid configuration")
            
            # Load CNAE green mapping
            self.load_cnae_green_mapping()
            
            # Setup DuckDB schema
            self.setup_duckdb_schema()
            
            # Load RFB data
            self.load_rfb_data()
            
            # Process green companies
            df = self.process_green_companies()
            
            if not df.empty:
                # Save to Parquet
                self.save_to_parquet(df)
                
                # Load to PostgreSQL
                self.load_to_postgres(df)
                
                logger.info(f"Pipeline completed successfully in {time.time() - start_time:.2f} seconds")
                logger.info(f"Processed {len(df)} green companies")
            else:
                logger.warning("No data to process")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

def main():
    """Main entry point."""
    try:
        with GreenJobsETL() as etl:
            etl.run_pipeline()
        
        return 0
        
    except Exception as e:
        logger.error(f"ETL execution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())