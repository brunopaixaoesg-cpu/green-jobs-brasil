from fastapi.testclient import TestClient
import importlib, sys, os

sys.path.insert(0, os.getcwd())
app = importlib.import_module('api.main').app
client = TestClient(app)
# Debug: listar rotas registradas que contêm 'empresas'
print('Registered routes (containing empresas):')
for r in app.routes:
	try:
		if 'empresas' in getattr(r, 'path', ''):
			print(' -', getattr(r, 'methods', ''), getattr(r, 'path', ''))
	except Exception:
		pass

resp = client.get('/empresas/lookup?cnpj=60.331.021/0001-11')
print('STATUS', resp.status_code)
print(resp.json())
