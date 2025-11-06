"""
Green Jobs Brasil - FastAPI Application
Main application file for the Green Jobs Brasil API.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session

from api.db import get_db, test_connection
from api.routers import companies, cnaes, stats, empresas, profissionais, vagas
from api.schemas import HealthResponse

# Create FastAPI application
app = FastAPI(
    title="Green Jobs Brasil API",
    description="API para consulta de empresas verdes no Brasil baseada em classificação CNAE e ODS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router)
app.include_router(cnaes.router)
app.include_router(stats.router)
app.include_router(empresas.router)
app.include_router(profissionais.router)
app.include_router(vagas.router)

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Green Jobs Brasil API",
        "version": "1.0.0",
        "description": "API para consulta de empresas verdes no Brasil",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns API status and database connectivity.
    """
    database_connected = test_connection()
    
    return HealthResponse(
        status="ok" if database_connected else "error",
        timestamp=datetime.now(),
        version="1.0.0",
        database_connected=database_connected
    )

@app.get("/info", tags=["info"])
async def api_info():
    """
    Get detailed API information and available endpoints.
    """
    return {
        "api_name": "Green Jobs Brasil",
        "version": "1.0.0",
        "description": "Sistema para identificação e classificação de empresas verdes no Brasil",
        "endpoints": {
            "empresas": {
                "GET /empresas": "Listar empresas verdes com filtros",
                "GET /empresas/{cnpj}": "Obter detalhes de uma empresa específica",
                "GET /empresas/stats/por-uf": "Estatísticas por UF",
                "GET /empresas/stats/por-porte": "Estatísticas por porte"
            },
            "cnaes": {
                "GET /cnaes": "Listar CNAEs verdes com filtros",
                "GET /cnaes/{cnae_code}": "Obter detalhes de um CNAE específico",
                "GET /cnaes/categorias/list": "Listar categorias disponíveis",
                "GET /cnaes/stats/resumo": "Estatísticas resumo dos CNAEs"
            },
            "stats": {
                "GET /stats": "Estatísticas completas do sistema",
                "GET /stats/dashboard/kpis": "KPIs principais para dashboard",
                "GET /stats/trends/crescimento": "Tendências de crescimento"
            }
        },
        "filters": {
            "empresas": ["uf", "municipio", "porte", "situacao", "cnae", "ods", "q"],
            "cnaes": ["categoria", "prioridade", "ods"]
        },
        "data_sources": [
            "Receita Federal do Brasil (RFB) - Dados Públicos CNPJ",
            "Classificação CNAE Verde customizada",
            "Mapeamento para Objetivos de Desenvolvimento Sustentável (ODS)"
        ]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint não encontrado", "detail": str(exc)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Erro interno do servidor", "detail": "Contate o administrador"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    from api.logger import logger
    logger.info("Green Jobs Brasil API iniciando...")
    logger.info("Verificando conectividade com banco de dados...")

    if test_connection():
        logger.info("Conexão com banco de dados estabelecida")
    else:
        logger.error("Falha na conexão com banco de dados")

    logger.info("API pronta para uso!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    from api.logger import logger
    logger.info("Green Jobs Brasil API encerrando...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )