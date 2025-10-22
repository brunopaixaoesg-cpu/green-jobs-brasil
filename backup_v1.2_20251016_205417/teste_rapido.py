"""
Teste Rápido de Todos os Endpoints
"""
import requests

base = 'http://127.0.0.1:8002'
print('🧪 TESTANDO TODOS OS ENDPOINTS...\n')

try:
    # Teste 1: Stats
    r = requests.get(f'{base}/api/stats')
    empresas = r.json()['empresas_verdes']
    print(f'✅ /api/stats: {r.status_code} - {empresas} empresas')

    # Teste 2: Empresas
    r = requests.get(f'{base}/api/empresas')
    qtd = len(r.json())
    print(f'✅ /api/empresas: {r.status_code} - {qtd} empresas retornadas')

    # Teste 3: CNPJ Correios
    r = requests.get(f'{base}/api/search-company/34028316000103')
    nome = r.json()['nome'][:40]
    print(f'✅ /api/search-company: {r.status_code} - {nome}...')

    # Teste 4: CNAEs
    r = requests.get(f'{base}/api/cnaes')
    qtd = len(r.json())
    print(f'✅ /api/cnaes: {r.status_code} - {qtd} CNAEs verdes')

    # Teste 5: Vagas
    r = requests.get(f'{base}/api/vagas')
    qtd = len(r.json())
    print(f'✅ /api/vagas: {r.status_code} - {qtd} vagas')

    # Teste 6: Profissionais
    r = requests.get(f'{base}/api/profissionais')
    qtd = len(r.json())
    print(f'✅ /api/profissionais: {r.status_code} - {qtd} profissionais')

    # Teste 7: Matching Stats
    r = requests.get(f'{base}/api/matching/stats')
    data = r.json()
    print(f'✅ /api/matching/stats: {r.status_code} - {data["total_candidaturas"]} candidaturas, ML {data["precisao_ml"]}%')

    print('\n🎉 TODOS OS 7 ENDPOINTS FUNCIONANDO!')
    print('\n🌐 Acesse: http://127.0.0.1:8002/')
    
except Exception as e:
    print(f'\n❌ Erro: {e}')
