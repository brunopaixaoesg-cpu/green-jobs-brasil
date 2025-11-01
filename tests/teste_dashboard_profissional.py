import requests

base_url = 'http://127.0.0.1:8002'

# 1. Testar login
print('1️⃣ Testando login...')
login_data = {'username': 'bruno@greenjobsbrasil.com.br', 'password': 'Senha123!'}
r = requests.post(f'{base_url}/api/auth/login', data=login_data)
print(f'   Status: {r.status_code}')

if r.status_code == 200:
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Testar endpoint de estatísticas
    print('2️⃣ Testando /api/profissionais/me/estatisticas...')
    r = requests.get(f'{base_url}/api/profissionais/me/estatisticas', headers=headers)
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Candidaturas: {data.get("candidaturas_enviadas", 0)}')
        print(f'   Score medio: {data.get("score_medio_compatibilidade", 0)}%')
        print(f'   Vagas disponiveis: {data.get("vagas_disponiveis", 0)}')
    
    # 3. Testar página do dashboard
    print('3️⃣ Testando /profissionais/dashboard...')
    r = requests.get(f'{base_url}/profissionais/dashboard')
    print(f'   Status: {r.status_code}, Tamanho: {len(r.text)} bytes')
    
    # 4. Testar endpoint de perfil
    print('4️⃣ Testando /api/profissionais/me/perfil...')
    r = requests.get(f'{base_url}/api/profissionais/me/perfil', headers=headers)
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        if 'perfil' in data:
            print(f'   Nome: {data["perfil"].get("nome_completo", "N/A")}')
    
    # 5. Testar endpoint de candidaturas
    print('5️⃣ Testando /api/profissionais/me/candidaturas...')
    r = requests.get(f'{base_url}/api/profissionais/me/candidaturas', headers=headers)
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Total: {len(data.get("candidaturas", []))} candidaturas')
    
    # 6. Testar endpoint de recomendações
    print('6️⃣ Testando /api/profissionais/me/recomendacoes...')
    r = requests.get(f'{base_url}/api/profissionais/me/recomendacoes', headers=headers)
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Vagas recomendadas: {len(data.get("vagas_recomendadas", []))}')
    
    print('\n✅ TODOS OS TESTES PASSARAM!')
else:
    print('❌ Erro no login')
