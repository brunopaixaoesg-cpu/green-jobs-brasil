"""
Green Jobs Brasil - Teste Final do Sistema
Verifica se todos os endpoints estão funcionando corretamente
"""
import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

def test_endpoint(endpoint, description):
    """Testa um endpoint da API"""
    try:
        print(f"\n🔍 Testando: {description}")
        print(f"   Endpoint: {endpoint}")
        
        response = requests.get(f"{API_BASE}{endpoint}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            
            if endpoint == "/empresas":
                print(f"   📊 Total empresas: {data.get('total', 0)}")
                print(f"   📋 Empresas retornadas: {len(data.get('items', []))}")
            elif endpoint == "/cnaes":
                print(f"   📊 Total CNAEs: {data.get('total', 0)}")
            elif endpoint == "/stats":
                print(f"   📊 Total empresas: {data.get('total_empresas', 0)}")
                print(f"   📊 Total CNAEs: {data.get('total_cnaes', 0)}")
                print(f"   🗺️ Estados: {len(data.get('empresas_por_uf', []))}")
            elif endpoint == "/health":
                print(f"   💚 Status: {data.get('status')}")
                print(f"   🗄️ Database: {data.get('database')}")
                print(f"   📊 Total empresas: {data.get('total_empresas', 0)}")
            else:
                print(f"   📄 Dados: {type(data)}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exceção: {str(e)}")

def main():
    print("🌱 GREEN JOBS BRASIL - TESTE FINAL DO SISTEMA")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Testar endpoints principais
    endpoints = [
        ("/", "Endpoint raiz"),
        ("/health", "Health check"),
        ("/empresas", "Listar empresas"),
        ("/cnaes", "Listar CNAEs"),
        ("/stats", "Estatísticas"),
        ("/empresas?uf=MG", "Filtrar empresas por UF"),
        ("/empresas?q=solar", "Buscar empresas por texto"),
        ("/cnaes?categoria=Energia", "Filtrar CNAEs por categoria")
    ]
    
    for endpoint, description in endpoints:
        test_endpoint(endpoint, description)
    
    print(f"\n{'=' * 50}")
    print("🎉 TESTE CONCLUÍDO!")
    print("📖 Acesse a documentação em: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()