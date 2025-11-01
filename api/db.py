"""api.db

Banco SQLite compartilhado e helpers de inicialização para o projeto
"""
import os
import sqlite3
from datetime import datetime
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gjb_dev.db")


def get_db():
    """Retorna uma conexão sqlite3 com row_factory configurado.

    Nota: check_same_thread=False facilita uso com Uvicorn em dev.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def test_connection() -> bool:
    """Testa conectividade básica com o banco. Retorna True se OK."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as ok")
        _ = cursor.fetchone()
        conn.close()
        return True
    except Exception:
        return False


def init_database():
    """Cria o schema mínimo necessário se não existir.

    Esta função é idempotente e segura para ser chamada na inicialização.
    """
    from api.logger import logger
    logger.info("Inicializando banco SQLite em: %s", DB_PATH)
    conn = get_db()
    cursor = conn.cursor()

    # Tabelas principais (versão compatível com os endpoints existentes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais_esg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            area_atuacao TEXT,
            experiencia_anos INTEGER DEFAULT 0,
            localizacao_cidade TEXT,
            localizacao_uf TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'ativo'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS storytelling (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profissional_id INTEGER,
            jornada_verde TEXT,
            motivacao TEXT,
            impacto TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profissional_id) REFERENCES profissionais_esg(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas_esg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT UNIQUE,
            razao_social TEXT,
            nome_fantasia TEXT,
            email TEXT UNIQUE,
            senha_hash TEXT,
            telefone TEXT,
            website TEXT,
            descricao TEXT,
            logo_url TEXT,
            score_verde REAL DEFAULT 0,
            ods_tags TEXT,
            cnaes_secundarias TEXT,
            status TEXT DEFAULT 'ativa',
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            cnpj TEXT,
            nivel_experiencia TEXT,
            tipo_contratacao TEXT,
            localizacao_cidade TEXT,
            localizacao_uf TEXT,
            remoto INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ativa',
            salario_min REAL,
            salario_max REAL,
            visualizacoes INTEGER DEFAULT 0,
            candidaturas_recebidas INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidaturas_esg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vaga_id INTEGER,
            profissional_id INTEGER,
            nome_completo TEXT,
            email TEXT,
            telefone TEXT,
            curriculo_texto TEXT,
            anos_experiencia_esg INTEGER DEFAULT 0,
            habilidades_esg TEXT,
            motivacao TEXT,
            compatibilidade_score REAL DEFAULT 0,
            status TEXT DEFAULT 'pendente',
            data_candidatura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observacoes TEXT,
            FOREIGN KEY (vaga_id) REFERENCES vagas(id),
            FOREIGN KEY (profissional_id) REFERENCES profissionais_esg(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vaga_id INTEGER,
            nome TEXT,
            email TEXT,
            telefone TEXT,
            curriculo TEXT,
            data_candidatura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (vaga_id) REFERENCES vagas(id)
        )
    """)

    # Cache simples para respostas da Receita Federal (TTL controlado pela aplicação)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receita_cache (
            cnpj TEXT PRIMARY KEY,
            response_json TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Auditoria de importações (quem/quando/payload/source)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            cnpj TEXT,
            action TEXT,
            source TEXT,
            payload_json TEXT,
            user_id TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            note TEXT
        )
    """)

    conn.commit()
    # Ensure backwards-compatible columns exist (idempotent)
    def _ensure_column(table: str, column: str, definition: str):
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        existing = [r[1] for r in cur.fetchall()]
        if column not in existing:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    try:
        _ensure_column('profissionais_esg', 'status', "TEXT DEFAULT 'ativo'")
    except Exception:
        # If ALTER TABLE not supported or other race, ignore (best-effort)
        pass

    # Ensure commonly added columns for empresas_esg (backwards-compatibility)
    try:
        _ensure_column('empresas_esg', 'ods_tags', 'TEXT')
        _ensure_column('empresas_esg', 'cnaes_secundarias', 'TEXT')
        _ensure_column('empresas_esg', 'score_verde', 'REAL DEFAULT 0')
    except Exception:
        # Best-effort; if ALTER TABLE cannot run, don't fail init
        pass

    conn.commit()
    conn.close()
    logger.info("Banco de dados inicializado (api.db.init_database)")


__all__ = ["get_db", "test_connection", "init_database", "DB_PATH"]
