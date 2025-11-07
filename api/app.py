"""
Green Jobs Brasil - FastAPI Application
Main application file for the Green Jobs Brasil API.
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any
from pydantic import BaseModel

from api.db import get_db, test_connection
from api.routers import companies, cnaes, stats, empresas, profissionais, vagas, health
from api.config import Config

# Configure rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI application
app = FastAPI(
    title="Green Jobs Brasil API",
    description="API para consulta de empresas verdes no Brasil baseada em classificação CNAE e ODS",
    version="1.6.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # HSTS - Force HTTPS in production
        if not Config.DEBUG:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP - Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "connect-src 'self' https://api.greenjobsbrasil.com.br;"
        )
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS Protection (legacy but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy (formerly Feature Policy)
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Configure CORS with environment variables
cors_origins = Config.get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=Config.CORS_ALLOW_CREDENTIALS,
    allow_methods=Config.CORS_ALLOW_METHODS.split(","),
    allow_headers=[Config.CORS_ALLOW_HEADERS] if Config.CORS_ALLOW_HEADERS != "*" else ["*"],
)

# Include routers
app.include_router(health.router)  # Health checks first
app.include_router(companies.router)
app.include_router(cnaes.router)
app.include_router(stats.router)
app.include_router(empresas.router)
app.include_router(profissionais.router)
app.include_router(vagas.router)

@app.get("/", tags=["root"])
@limiter.limit(f"{Config.RATE_LIMIT_PER_SECOND}/second")
async def root(request: Request):
    """
    Root endpoint with API information.
    """
    return {
        "message": "Green Jobs Brasil API",
        "version": "1.6.0",
        "description": "API para consulta de empresas verdes no Brasil",
        "docs": "/docs",
        "health": "/health",
        "security": {
            "rate_limit": f"{Config.RATE_LIMIT_PER_SECOND} req/s per IP",
            "cors_enabled": True,
            "https_required": not Config.DEBUG
        }
    }

@app.get("/info", tags=["info"])
@limiter.limit(f"{Config.RATE_LIMIT_PER_SECOND}/second")
async def api_info(request: Request):
    """
    Get detailed API information and available endpoints.
    """
    return {
        "api_name": "Green Jobs Brasil",
        "version": "1.6.0",
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
        ],
        "security": {
            "rate_limit_per_second": Config.RATE_LIMIT_PER_SECOND,
            "rate_limit_per_minute": Config.RATE_LIMIT_PER_MINUTE,
            "rate_limit_per_hour": Config.RATE_LIMIT_PER_HOUR,
            "cors_origins": Config.get_cors_origins(),
            "https_only": not Config.DEBUG
        }
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