from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="Green Jobs Brasil API - Teste")

@app.get("/")
def root():
    return {
        "message": "Green Jobs Brasil API", 
        "status": "running", 
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    return {
        "status": "ok", 
        "timestamp": datetime.now().isoformat()
    }

@app.get("/empresas")
def empresas(uf: str = None, q: str = None):
    # Dados de exemplo para teste
    empresas_exemplo = [
        {
            "cnpj": "12345678000195",
            "razao_social": "Solar Energy Brasil Ltda",
            "uf": "MG",
            "cnae_principal": "3511-5/02",
            "score_verde": 80
        },
        {
            "cnpj": "98765432000123", 
            "razao_social": "Energia Solar do Norte",
            "uf": "MG",
            "cnae_principal": "3511-5/02", 
            "score_verde": 85
        },
        {
            "cnpj": "11223344000167",
            "razao_social": "Reciclagem Verde SA", 
            "uf": "RJ",
            "cnae_principal": "3831-9/00",
            "score_verde": 75
        }
    ]
    
    result = empresas_exemplo
    
    # Filtrar por UF se fornecido
    if uf:
        result = [e for e in result if e["uf"] == uf.upper()]
    
    # Filtrar por texto se fornecido  
    if q:
        result = [e for e in result if q.lower() in e["razao_social"].lower()]
    
    return {
        "items": result,
        "total": len(result),
        "filters": {"uf": uf, "q": q}
    }

@app.get("/cnaes")
def cnaes():
    return {
        "items": [
            {"cnae": "3511-5/02", "titulo": "Geração de energia elétrica - Solar", "categoria": "Energia Renovável"},
            {"cnae": "3831-9/00", "titulo": "Recuperação de materiais metálicos", "categoria": "Economia Circular"}
        ],
        "total": 2
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)