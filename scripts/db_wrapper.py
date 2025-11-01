import os
import sqlite3
from contextlib import contextmanager

# Central DB wrapper for scripts to use the same DB path as the API
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.environ.get('GJB_DB_PATH', os.path.join(BASE_DIR, 'api', 'gjb_dev.db'))

@contextmanager
def get_connection(check_same_thread=False):
    """Yield a sqlite3.Connection to the canonical DB path.

    Usage:
        with get_connection() as conn:
            cursor = conn.cursor()
            ...
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=check_same_thread)
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:
            pass
