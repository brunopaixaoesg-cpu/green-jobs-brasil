"""Ponto de entrada unificado para a API.

Este módulo reexporta a aplicação FastAPI definida em
`api/sqlite_api_clean.py` e garante que o banco esteja inicializado.
"""
from api import sqlite_api_clean as _sqlite
from api.db import init_database
from api.settings import settings
from api.logger_setup import get_logger

logger = get_logger(__name__)

# Inicializar esquema mínimo (idempotente)
init_database()

# Reexportar a instância do FastAPI
app = _sqlite.app

# Incluir routers do pacote `api.routers` quando disponíveis.
try:
	from api.routers import auth as auth_router
	app.include_router(auth_router.router)
	logger.info("✓ Router auth registrado")
except Exception as e:
	logger.warning(f"Router auth não carregado: {e}")

# Incluir router de health checks
try:
	from api.routers import health as health_router
	app.include_router(health_router.router)
	logger.info("✓ Router health registrado")
except Exception as e:
	logger.warning(f"Router health não carregado: {e}")

# Incluir router TSB (se habilitado)
if settings.enable_tsb:
	try:
		from api.routers import taxonomia as taxonomia_router
		app.include_router(taxonomia_router.router)
		logger.info("✓ Router taxonomia TSB registrado")
	except Exception as e:
		logger.error(f"Router taxonomia TSB falhou: {e}")
else:
	logger.info("TSB desabilitado via configuração")

__all__ = ["app"]
