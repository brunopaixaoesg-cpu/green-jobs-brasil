from fastapi import FastAPI, HTTPException
import sqlite3
import uvicorn
from datetime import datetime

app = FastAPI()

DATABASE_PATH = "gjb_dev.db"

def get_db_connection():
    """Obter conexão com banco SQLite"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")

@app.get("/test-stats")
def test_stats():
    """Testar stats com logging detalhado"""
    try:
        print("=== Iniciando test_stats ===")
        conn = get_db_connection()
        cursor = conn.cursor()
        print("Conexão estabelecida")
        
        # Total de empresas
        cursor.execute("SELECT count(*) as total FROM empresas_verdes")
        result1 = cursor.fetchone()
        total_empresas = result1["total"]
        print(f"Total empresas: {total_empresas}")
        
        # Total de CNAEs
        cursor.execute("SELECT count(*) as total FROM cnae_green")
        result2 = cursor.fetchone()
        total_cnaes = result2["total"]
        print(f"Total CNAEs: {total_cnaes}")
        
        # Score médio das empresas
        cursor.execute("SELECT AVG(score_verde) as media FROM empresas_verdes")
        result3 = cursor.fetchone()
        score_medio = result3["media"] or 0
        print(f"Score médio: {score_medio}")
        
        # Total de relações empresa-cnae
        cursor.execute("SELECT count(*) as total FROM empresa_cnae")
        result4 = cursor.fetchone()
        total_relacoes = result4["total"]
        print(f"Total relações: {total_relacoes}")
        
        conn.close()
        print("Conexão fechada")
        
        response = {
            "total_empresas": total_empresas,
            "total_cnaes_verdes": total_cnaes,
            "score_medio": float(score_medio),
            "total_relacoes": total_relacoes,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Response: {response}")
        return response
        
    except Exception as e:
        error_msg = f"Erro ao obter estatísticas: {str(e)}"
        print(f"ERRO: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    print("Iniciando API de teste...")
    uvicorn.run(app, host="127.0.0.1", port=8001)