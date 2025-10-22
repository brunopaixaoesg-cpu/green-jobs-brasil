import requests

# Testar admin
print("Testando Admin...")
r = requests.post('http://127.0.0.1:8002/api/auth/login', 
                  data={'username': 'admin@greenjobs.com.br', 'password': 'admin123'})
print(f"Admin Status: {r.status_code}")
if r.status_code == 200:
    token = r.json()['access_token']
    print(f"Token OK!")
    
    # Buscar dados
    user_r = requests.get('http://127.0.0.1:8002/api/auth/me', 
                          headers={'Authorization': f'Bearer {token}'})
    print(f"User: {user_r.json()['full_name']}")

print()

# Testar Bruno
print("Testando Bruno...")
r = requests.post('http://127.0.0.1:8002/api/auth/login', 
                  data={'username': 'bruno@greenjobsbrasil.com.br', 'password': 'Senha123!'})
print(f"Bruno Status: {r.status_code}")
if r.status_code != 200:
    print(f"Erro: {r.json()['detail']}")
else:
    print("Login OK!")
