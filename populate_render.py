"""
Script para popular PostgreSQL no Render via API
Envia dados diretamente para os endpoints do deploy
"""
import requests
import json

BASE_URL = "https://greenjobs-brasil.onrender.com"

def test_connection():
    """Testa se API está online"""
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            print("✅ API online:", response.json())
            return True
    except Exception as e:
        print("❌ Erro de conexão:", e)
    return False

def populate_via_api():
    """Popula dados via chamadas diretas à API"""
    
    # 1. Testar conexão
    if not test_connection():
        return
    
    # 2. Popular dados diretamente no PostgreSQL
    print("📊 Populando via trigger interno...")
    
    # Chamar endpoint especial para seed
    try:
        response = requests.post(f"{BASE_URL}/api/seed")
        if response.status_code == 200:
            print("✅ Dados populados com sucesso!")
        else:
            print(f"⚠️ Erro ao popular: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    populate_via_api()