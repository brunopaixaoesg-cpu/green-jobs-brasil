from fastapi.testclient import TestClient
import importlib, sys, os, json
sys.path.insert(0, os.getcwd())
app = importlib.import_module('api.main').app
client = TestClient(app)

endpoints = [
    ('GET','/docs'),
    ('GET','/api/status'),
    ('GET','/api/populate'),
    ('GET','/api/empresas'),
    ('GET','/api/vagas'),
    ('GET','/api/profissionais'),
    ('GET','/api/candidaturas'),
    ('GET','/api/matching/stats'),
    ('GET','/api/matching/dashboard')
]

results = []

print('Starting full smoke test...')
for method, path in endpoints:
    try:
        if method == 'GET':
            r = client.get(path)
        else:
            r = client.post(path)
        status = r.status_code
        summary = None
        try:
            j = r.json()
            if isinstance(j, list):
                summary = f'list len={len(j)}'
            elif isinstance(j, dict):
                summary = 'keys=' + ','.join(list(j.keys())[:5])
            else:
                summary = str(type(j))
        except Exception:
            text = (r.text or '')
            summary = text.replace('\n',' ')[:200]
        print(f'{path} -> {status} | {summary}')
        results.append((path, status, summary))
    except Exception as e:
        print(f'{path} -> ERROR: {e}')
        results.append((path, 'ERROR', str(e)))

# Run auth flow too (reuse existing test if available)
print('\nRunning auth flow test (register/login/me)')
from random import randint
email = f'full_smoke_{randint(1000,9999)}@example.com'
password = 'SmokeTest123'

# Register
r = client.post('/api/auth/register', json={
    'email': email,
    'password': password,
    'full_name': 'Smoke Test',
    'user_type': 'profissional'
})
print('/api/auth/register', r.status_code, getattr(r,'text', '')[:200])

# Login JSON
r2 = client.post('/api/auth/login-json', json={'email': email, 'password': password})
print('/api/auth/login-json', r2.status_code)
if r2.status_code == 200:
    try:
        tok = r2.json().get('access_token')
        h = {'Authorization': f'Bearer {tok}'}
        me = client.get('/api/auth/me', headers=h)
        print('/api/auth/me', me.status_code, (me.json() if me.status_code==200 else me.text) )
    except Exception as e:
        print('Error parsing token or /me:', e)

print('\nFull smoke test completed.')

# Summarize failures
fails = [r for r in results if not (isinstance(r[1], int) and 200 <= r[1] < 300)]
print('\nSummary:')
print('Total endpoints checked:', len(results))
print('Failures:', len(fails))
for f in fails:
    print(' -', f)

if len(fails) > 0:
    raise SystemExit(1)
else:
    raise SystemExit(0)
