import sqlite3, os, json
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.join(BASE, 'api', 'gjb_dev.db')
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
try:
    cur.execute('SELECT cnpj, substr(response_json,1,200) as snippet, fetched_at FROM receita_cache ORDER BY fetched_at DESC LIMIT 10')
    rows = cur.fetchall()
    for r in rows:
        print(dict(r))
finally:
    conn.close()
