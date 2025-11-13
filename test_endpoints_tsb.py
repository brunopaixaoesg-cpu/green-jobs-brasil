"""
Script para testar endpoints TSB da API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print("=" * 80)
print("TESTE ENDPOINTS TSB - Green Jobs Brasil")
print("=" * 80)

# Teste 1: /api/taxonomia/objetivos
print("\n1. GET /api/taxonomia/objetivos")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/taxonomia/objetivos", timeout=5)
    if response.status_code == 200:
        objetivos = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total de objetivos: {len(objetivos)}")
        print(f"✓ Primeiro objetivo: {objetivos[0]['codigo']} - {objetivos[0]['nome']}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 2: /api/taxonomia/setores
print("\n2. GET /api/taxonomia/setores")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/taxonomia/setores", timeout=5)
    if response.status_code == 200:
        setores = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total de setores: {len(setores)}")
        print(f"✓ Primeiro setor: {setores[0]['nome']}")
        print(f"  - Subsetores: {len(setores[0].get('subsetores', []))}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 3: /api/taxonomia/criterios
print("\n3. GET /api/taxonomia/criterios")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/taxonomia/criterios", timeout=5)
    if response.status_code == 200:
        criterios = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total de critérios: {len(criterios)}")
        for crit in criterios:
            print(f"  - {crit['codigo']}: {crit['peso']} pontos")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 4: /api/taxonomia/info
print("\n4. GET /api/taxonomia/info")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/taxonomia/info", timeout=5)
    if response.status_code == 200:
        info = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"  - Nome: {info['nome']}")
        print(f"  - Versão: {info['versao']}")
        print(f"  - Total objetivos: {info['totais']['objetivos']}")
        print(f"  - Total setores: {info['totais']['setores']}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 5: /api/empresas (sem TSB)
print("\n5. GET /api/empresas (sem TSB)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/empresas", timeout=5)
    if response.status_code == 200:
        empresas = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total de empresas: {len(empresas)}")
        if len(empresas) > 0:
            print(f"✓ Primeira empresa: {empresas[0].get('razao_social', 'N/A')}")
            print(f"  - Tem TSB no response? {'tsb_elegivel' in empresas[0]}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 6: /api/empresas?tsb=true (com TSB)
print("\n6. GET /api/empresas?tsb=true (com enriquecimento TSB)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/empresas?tsb=true", timeout=5)
    if response.status_code == 200:
        empresas = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Total de empresas: {len(empresas)}")
        if len(empresas) > 0:
            empresa = empresas[0]
            print(f"✓ Primeira empresa: {empresa.get('razao_social', 'N/A')}")
            print(f"  - TSB Elegível: {empresa.get('tsb_elegivel', False)}")
            print(f"  - TSB Score: {empresa.get('tsb_score', 0)}")
            print(f"  - TSB Badge: {empresa.get('tsb_badge', 'N/A')}")
            print(f"  - TSB Objetivos: {empresa.get('tsb_objetivos', [])}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

# Teste 7: /health
print("\n7. GET /health")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        health = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"  - Banco: {health.get('database', 'N/A')}")
        print(f"  - TSB Enabled: {health.get('features', {}).get('tsb', 'N/A')}")
    else:
        print(f"✗ Erro {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Erro na requisição: {e}")

print("\n" + "=" * 80)
print("TESTES CONCLUÍDOS")
print("=" * 80)
print("\n💡 Acesse http://127.0.0.1:8000/docs para ver a documentação completa!")
