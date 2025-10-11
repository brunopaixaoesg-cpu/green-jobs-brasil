"""
Green Jobs Brasil - Teste Simples da API
Versão simplificada para teste inicial sem dependência do banco.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Create FastAPI application
app = FastAPI(
    title="Green Jobs Brasil API - Teste",
    description="API para consulta de empresas verdes no Brasil",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint com informações da API."""
    return {
        "message": "Green Jobs Brasil API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database_connected": False  # Para teste inicial
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint de teste."""
    return {
        "message": "API funcionando corretamente!",
        "timestamp": datetime.now().isoformat(),
        "endpoints_disponiveis": [
            "GET /",
            "GET /health", 
            "GET /test",
            "GET /docs (documentação Swagger)"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)