"""Ponto de entrada unificado para a API.

Este módulo reexporta a aplicação FastAPI definida em
`api/sqlite_api_clean.py` e garante que o banco esteja inicializado.
"""
from api import sqlite_api_clean as _sqlite
from api.db import init_database

# Inicializar esquema mínimo (idempotente)
init_database()

# Reexportar a instância do FastAPI
app = _sqlite.app

# Incluir routers do pacote `api.routers` quando disponíveis.
try:
	from api.routers import auth as auth_router
	app.include_router(auth_router.router)
except Exception:
	# Routers opcionais podem falhar durante refactor; continue silenciosamente
	pass

__all__ = ["app"]
