import requests
import json

def testar_api_vagas():
    """Testa se a API está retornando as vagas"""
    try:
        print("🧪 Testando API de vagas...")
        response = requests.get("http://127.0.0.1:8002/api/vagas")
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total de vagas: {data.get('total', 0)}")
            
            vagas = data.get('vagas', [])
            if vagas:
                print(f"✅ {len(vagas)} vagas encontradas:")
                for i, vaga in enumerate(vagas[:3], 1):  # Mostrar primeiras 3
                    print(f"   {i}. {vaga.get('titulo')} - {vaga.get('empresa_nome', 'N/A')}")
                    print(f"      📍 {vaga.get('localizacao_cidade', 'N/A')}, {vaga.get('localizacao_uf', 'N/A')}")
                    print(f"      💰 R$ {vaga.get('salario_min', 0)} - R$ {vaga.get('salario_max', 0)}")
                    print(f"      📝 {vaga.get('nivel_experiencia', 'N/A')} | {vaga.get('tipo_contratacao', 'N/A')}")
                    print()
            else:
                print("❌ Nenhuma vaga encontrada")
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando em http://127.0.0.1:8002")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    testar_api_vagas()