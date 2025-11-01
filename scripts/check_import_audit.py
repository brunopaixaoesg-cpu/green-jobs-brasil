import sqlite3, os, json, sys
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.join(BASE, 'api', 'gjb_dev.db')
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
try:
    cur.execute('SELECT id, empresa_id, cnpj, action, source, payload_json, imported_at, note FROM import_audit ORDER BY imported_at DESC LIMIT 10')
    rows = cur.fetchall()
    for r in rows:
        print(dict(r))
finally:
    conn.close()
