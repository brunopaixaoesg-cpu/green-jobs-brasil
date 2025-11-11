from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.sqlite_api_clean import app

client = TestClient(app)

# List cache (should be local)
r = client.get('/api/admin/receita-cache')
print('receita-cache list:', r.status_code, r.json())

# List audit
r2 = client.get('/api/admin/import-audit')
print('import-audit list:', r2.status_code, r2.json())

# Purge cache (delete all)
r3 = client.delete('/api/admin/receita-cache')
print('purge cache:', r3.status_code, r3.json())
