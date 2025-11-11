from fastapi.testclient import TestClient
import importlib, sys, os, random
sys.path.insert(0, os.getcwd())
app = importlib.import_module('api.main').app
client = TestClient(app)

email = f"test_user_{random.randint(1000,9999)}@example.com"
password = "Test1234"

print('Registering user:', email)
resp = client.post('/api/auth/register', json={
    'email': email,
    'password': password,
    'full_name': 'Test User',
    'user_type': 'profissional'
})
print('register status', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text[:500])

print('Logging in (json)')
resp2 = client.post('/api/auth/login-json', json={'email': email, 'password': password})
print('login status', resp2.status_code)
try:
    print(resp2.json())
except Exception:
    print(resp2.text[:500])

# If login succeeded, try /api/auth/me
if resp2.status_code == 200:
    token = resp2.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    me = client.get('/api/auth/me', headers=headers)
    print('/api/auth/me', me.status_code)
    try:
        print(me.json())
    except Exception:
        print(me.text[:500])
