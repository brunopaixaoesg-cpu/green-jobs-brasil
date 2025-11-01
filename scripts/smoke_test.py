from fastapi.testclient import TestClient
import importlib, sys, os

# Ensure repo root is on sys.path so `api` package can be imported when running
# the script from anywhere (helps TestClient imports)
sys.path.insert(0, os.getcwd())

app = importlib.import_module('api.main').app
client = TestClient(app)
paths=['/docs','/api/status','/api/populate','/api/empresas']

for p in paths:
    r = client.get(p)
    print(p, r.status_code)
    txt = r.text or ''
    print(txt.replace('\n',' ')[:400])
