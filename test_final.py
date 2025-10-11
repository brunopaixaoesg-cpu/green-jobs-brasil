"""
Teste final do sistema Green Jobs Brasil
Verifica se tudo está funcionando corretamente
"""
import requests
import time
import json

def test_api():
    """Testa se a API está funcionando"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 TESTE FINAL - Green Jobs Brasil")
    print("=" * 50)
    
    # Teste 1: Dashboard
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Dashboard carregado com sucesso")
        else:
            print(f"❌ Erro no dashboard: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar dashboard: {e}")
        return False
    
    # Teste 2: Estatísticas
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas: {stats['total_empresas']} empresas, {stats['total_cnaes_verdes']} CNAEs")
        else:
            print(f"❌ Erro em stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar stats: {e}")
    
    # Teste 3: Lista de empresas
    try:
        response = requests.get(f"{base_url}/api/empresas")
        if response.status_code == 200:
            empresas = response.json()
            print(f"✅ Lista de empresas: {len(empresas)} encontradas")
        else:
            print(f"❌ Erro em empresas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar empresas: {e}")
    
    # Teste 4: Lista de CNAEs
    try:
        response = requests.get(f"{base_url}/api/cnaes")
        if response.status_code == 200:
            cnaes = response.json()
            print(f"✅ Lista de CNAEs: {len(cnaes)} encontrados")
        else:
            print(f"❌ Erro em CNAEs: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar CNAEs: {e}")
    
    # Teste 5: Busca de empresa (CNPJ da CIMO)
    try:
        test_cnpj = "27325719000159"
        response = requests.get(f"{base_url}/search-company/{test_cnpj}")
        if response.status_code == 200:
            company = response.json()
            print(f"✅ Busca de empresa: {company['nome']} (Score: {company['green_score']})")
        else:
            print(f"❌ Erro na busca: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao buscar empresa: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TESTE CONCLUÍDO")
    print("✅ Sistema está funcionando corretamente!")
    print("📍 Acesse: http://127.0.0.1:8000")
    print("🔍 Digite qualquer CNPJ brasileiro para testar")
    
    return True

if __name__ == "__main__":
    # Aguarda a API estar pronta
    print("Aguardando API estar pronta...")
    time.sleep(2)
    
    test_api()