"""
ETL Simplificado - Carrega dados diretamente no SQLite
"""
import sqlite3
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_simple_etl():
    """Executa ETL simplificado direto no SQLite."""
    try:
        # Conectar ao banco
        conn = sqlite3.connect('gjb_dev.db')
        cursor = conn.cursor()
        
        logger.info("🔄 Iniciando ETL simplificado...")
        
        # Limpar dados existentes
        cursor.execute("DELETE FROM empresas_verdes")
        cursor.execute("DELETE FROM empresa_cnae")
        
        # Dados de exemplo de empresas verdes
        empresas_exemplo = [
            ("12345678000195", "Solar Energy Brasil Ltda", "Solar Energy Brasil", "3511-5/02", '["3511-5/01","3512-3/01"]', "03", "MG", "Belo Horizonte", "ATIVA", "2020-01-15", 80, '[7,13]'),
            ("98765432000123", "Reciclagem Verde SA", "Reciclagem Verde", "3831-9/00", '["3832-7/00"]', "02", "RJ", "Rio de Janeiro", "ATIVA", "2019-05-20", 75, '[8,12]'),
            ("11223344000167", "Tratamento de Água Limpa Ltda", "Água Limpa", "3600-6/01", '[]', "03", "SP", "São Paulo", "ATIVA", "2018-03-10", 80, '[6,14]'),
            ("55667788000145", "Energia Eólica do Norte SA", "Eólica Norte", "3511-5/03", '[]', "04", "RJ", "Niterói", "ATIVA", "2021-07-01", 80, '[7,13]'),
            ("99887766000134", "Consultoria Sustentável Ltda", "Consultoria Verde", "7490-1/04", '[]', "01", "MG", "Uberlândia", "ATIVA", "2022-02-28", 60, '[8,12]'),
            ("88776655000178", "Biomassa Energia Verde SA", "Biomassa Energia", "3511-5/04", '["3600-6/01"]', "04", "MG", "Juiz de Fora", "ATIVA", "2020-08-15", 90, '[7,13,15]'),
            ("77665544000189", "Coleta Seletiva MG Ltda", "Coleta Seletiva", "3811-4/00", '["3831-9/00"]', "02", "MG", "Contagem", "ATIVA", "2021-03-20", 90, '[11,12]'),
            ("66554433000190", "Hidrelétrica Sustentável SA", "Hidrelétrica Verde", "3511-5/01", '[]', "04", "RJ", "Teresópolis", "ATIVA", "2019-11-10", 80, '[7,13]'),
            ("55443322000101", "Gestão de Resíduos SP Ltda", "Gestão Resíduos", "3821-1/00", '["3822-0/00"]', "03", "SP", "Guarulhos", "ATIVA", "2020-05-25", 90, '[11,12]'),
            ("44332211000112", "Energia Solar RJ SA", "Solar RJ", "3511-5/02", '["3513-1/01"]', "03", "RJ", "Rio de Janeiro", "ATIVA", "2021-09-30", 90, '[7,13]'),
        ]
        
        # Inserir empresas
        for empresa in empresas_exemplo:
            cursor.execute("""
                INSERT INTO empresas_verdes 
                (cnpj, razao_social, nome_fantasia, cnae_principal, cnaes_secundarias,
                 porte, uf, municipio, situacao_cadastral, data_abertura, score_verde,
                 ods_tags, fonte_atualizacao, atualizado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, empresa + ("ETL_DEMO", datetime.now().isoformat()))
        
        # Inserir relacionamentos empresa-cnae
        for empresa in empresas_exemplo:
            cnpj = empresa[0]
            cnae_principal = empresa[3]
            cnaes_secundarias = json.loads(empresa[4])
            
            # CNAE principal
            cursor.execute("""
                INSERT OR IGNORE INTO empresa_cnae (cnpj, codigo_cnae)
                VALUES (?, ?)
            """, (cnpj, cnae_principal))
            
            # CNAEs secundárias
            for cnae in cnaes_secundarias:
                cursor.execute("""
                    INSERT OR IGNORE INTO empresa_cnae (cnpj, codigo_cnae)
                    VALUES (?, ?)
                """, (cnpj, cnae))
        
        conn.commit()
        
        # Verificar dados carregados
        cursor.execute("SELECT COUNT(*) FROM empresas_verdes")
        empresas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empresa_cnae")
        relacoes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cnae_green")
        cnaes_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"✅ ETL concluído com sucesso!")
        logger.info(f"📊 Dados carregados:")
        logger.info(f"  - {empresas_count} empresas verdes")
        logger.info(f"  - {relacoes_count} relacionamentos empresa-CNAE")
        logger.info(f"  - {cnaes_count} CNAEs classificados")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no ETL: {e}")
        return False

if __name__ == "__main__":
    if run_simple_etl():
        logger.info("🎉 Pronto para usar a API completa!")
    else:
        logger.error("❌ Falha no ETL")