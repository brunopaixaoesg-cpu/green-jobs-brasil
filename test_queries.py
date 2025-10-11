import sqlite3
import sys
import os

# Caminho para o banco
if os.path.exists("gjb_dev.db"):
    DATABASE_PATH = "gjb_dev.db"
elif os.path.exists("../gjb_dev.db"):
    DATABASE_PATH = "../gjb_dev.db"
else:
    print("Banco de dados não encontrado!")
    sys.exit(1)

def test_queries():
    """Testar queries do sistema"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("=== TESTE 1: Stats ===")
        try:
            # Total de empresas
            cursor.execute("SELECT count(*) as total FROM empresas_verdes")
            total_empresas = cursor.fetchone()["total"]
            print(f"Total empresas: {total_empresas}")
            
            # Total de CNAEs
            cursor.execute("SELECT count(*) as total FROM cnae_green")
            total_cnaes = cursor.fetchone()["total"]
            print(f"Total CNAEs: {total_cnaes}")
            
            # Score médio das empresas
            cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
            score_medio = cursor.fetchone()["media"] or 0
            print(f"Score médio: {score_medio}")
            
            # Total de relações empresa-cnae
            cursor.execute("SELECT count(*) as total FROM empresa_cnae")
            total_relacoes = cursor.fetchone()["total"]
            print(f"Total relações: {total_relacoes}")
            
        except Exception as e:
            print(f"ERRO em Stats: {e}")
        
        print("\n=== TESTE 2: Empresas ===")
        try:
            query = """
            SELECT cnpj, razao_social, nome_fantasia, cnae_principal, 
                   porte, uf, municipio, situacao_cadastral, score_verde as green_score,
                   data_abertura, fonte_atualizacao, atualizado_em
            FROM empresas_verdes 
            WHERE 1=1
            ORDER BY score_verde DESC LIMIT 5
            """
            cursor.execute(query)
            empresas = [dict(row) for row in cursor.fetchall()]
            print(f"Encontradas {len(empresas)} empresas")
            if empresas:
                print(f"Primeira empresa: {empresas[0]['razao_social']}")
                
        except Exception as e:
            print(f"ERRO em Empresas: {e}")
        
        print("\n=== TESTE 3: CNAEs ===")
        try:
            query = """
            SELECT cnae as codigo, titulo as descricao, categoria as classificacao, 
                   prioridade, ods_raw as ods, observacoes, created_at
            FROM cnae_green 
            WHERE 1=1
            LIMIT 5
            """
            cursor.execute(query)
            cnaes = [dict(row) for row in cursor.fetchall()]
            print(f"Encontrados {len(cnaes)} CNAEs")
            if cnaes:
                print(f"Primeiro CNAE: {cnaes[0]['codigo']} - {cnaes[0]['descricao']}")
                
        except Exception as e:
            print(f"ERRO em CNAEs: {e}")
        
        conn.close()
        print("\n=== TESTE CONCLUÍDO ===")
        
    except Exception as e:
        print(f"ERRO GERAL: {e}")

if __name__ == "__main__":
    test_queries()