"""
Teste completo das funcionalidades da API Green Jobs Brasil
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def test_api():
    print("🧪 Testando Green Jobs Brasil API")
    print("=" * 50)
    
    # 1. Teste básico
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Página inicial: {response.status_code}")
    except Exception as e:
        print(f"❌ Página inicial: {e}")
    
    # 2. Teste empresas
    try:
        response = requests.get(f"{BASE_URL}/api/empresas")
        data = response.json()
        print(f"✅ Empresas: {len(data)} empresas encontradas")
    except Exception as e:
        print(f"❌ Empresas: {e}")
    
    # 3. Teste estatísticas
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        data = response.json()
        print(f"✅ Estatísticas: {data}")
    except Exception as e:
        print(f"❌ Estatísticas: {e}")
    
    # 4. Teste CNPJ search
    try:
        cnpj_teste = "12345678000195"
        response = requests.get(f"{BASE_URL}/api/search-company/{cnpj_teste}")
        print(f"✅ Busca CNPJ: {response.status_code} - {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Busca CNPJ: {e}")
    
    # 5. Teste matching stats
    try:
        response = requests.get(f"{BASE_URL}/api/matching/stats")
        data = response.json()
        print(f"✅ Matching Stats: {data}")
    except Exception as e:
        print(f"❌ Matching Stats: {e}")
    
    # 6. Teste vagas
    try:
        response = requests.get(f"{BASE_URL}/api/vagas")
        data = response.json()
        print(f"✅ Vagas: {len(data)} vagas encontradas")
    except Exception as e:
        print(f"❌ Vagas: {e}")
    
    # 7. Teste profissionais
    try:
        response = requests.get(f"{BASE_URL}/api/profissionais")
        data = response.json()
        print(f"✅ Profissionais: {len(data)} profissionais encontrados")
    except Exception as e:
        print(f"❌ Profissionais: {e}")
    
    print("=" * 50)
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    test_api()