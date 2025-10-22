#!/usr/bin/env python3
"""
Módulo de banco de dados para API
"""

import sqlite3
from typing import Dict, Any

DB_PATH = "gjb_dev.db"

def get_db():
    """Obter conexão com banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def test_connection():
    """Testar conexão com banco de dados"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'")
        result = cursor.fetchone()
        conn.close()
        return True, f"Conexão OK - {result['count']} tabelas encontradas"
    except Exception as e:
        return False, f"Erro de conexão: {str(e)}"

def dict_factory(cursor, row):
    """Factory para retornar resultados como dict"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}