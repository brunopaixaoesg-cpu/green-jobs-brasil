#!/usr/bin/env python3
"""
Módulo de banco de dados para API - PostgreSQL
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

def get_database_url() -> str:
    """Obter URL do banco de dados (PostgreSQL no Render, SQLite local)"""
    return os.getenv("DATABASE_URL", "sqlite:///gjb_dev.db")

def get_db():
    """Obter conexão com banco de dados PostgreSQL"""
    database_url = get_database_url()
    
    # Se for PostgreSQL (Render)
    if database_url.startswith("postgres://") or database_url.startswith("postgresql://"):
        # Render usa postgres://, mas psycopg2 precisa de postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn
    
    # Fallback para SQLite local (desenvolvimento)
    else:
        import sqlite3
        conn = sqlite3.connect("gjb_dev.db")
        conn.row_factory = sqlite3.Row
        return conn

def test_connection():
    """Testar conexão com banco de dados"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        database_url = get_database_url()
        if database_url.startswith("postgres"):
            cursor.execute("SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = 'public'")
        else:
            cursor.execute("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'")
        
        result = cursor.fetchone()
        count = result['count'] if isinstance(result, dict) else result[0]
        conn.close()
        return True, f"Conexão OK - {count} tabelas encontradas"
    except Exception as e:
        return False, f"Erro de conexão: {str(e)}"