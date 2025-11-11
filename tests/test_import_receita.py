from fastapi.testclient import TestClient
import sys
import os
# garantir que o diretório do projeto esteja no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.sqlite_api_clean import app

client = TestClient(app)

resp = client.post('/api/empresas/import-receita', json={'cnpj': '60.331.021/0001-11'})
print(resp.status_code)
print(resp.json())
