"""
Teste de Segurança P3.2 - CORS, Rate Limiting e Security Headers
"""
import requests
import time
from typing import Dict

BASE_URL = "http://127.0.0.1:8002"

def test_security_headers():
    """Testa se os security headers estão presentes"""
    print("\n🔒 Testando Security Headers...")
    
    response = requests.get(f"{BASE_URL}/")
    headers = response.headers
    
    required_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": None,  # Apenas verificar presença
        "Permissions-Policy": None
    }
    
    print(f"Status: {response.status_code}")
    
    for header, expected_value in required_headers.items():
        if header in headers:
            actual_value = headers[header]
            if expected_value is None or expected_value in actual_value:
                print(f"  ✅ {header}: {actual_value[:60]}...")
            else:
                print(f"  ❌ {header}: Esperado '{expected_value}', recebido '{actual_value}'")
        else:
            print(f"  ❌ {header}: Header ausente")
    
    # HSTS só deve estar presente em produção (DEBUG=false)
    if "Strict-Transport-Security" in headers:
        print(f"  ℹ️  Strict-Transport-Security: {headers['Strict-Transport-Security']} (produção)")
    else:
        print(f"  ℹ️  Strict-Transport-Security: Ausente (desenvolvimento)")

def test_cors_headers():
    """Testa se os CORS headers estão configurados"""
    print("\n🌐 Testando CORS Headers...")
    
    # OPTIONS request para verificar CORS
    headers = {"Origin": "http://localhost:3000"}
    response = requests.options(f"{BASE_URL}/", headers=headers)
    
    cors_headers = response.headers
    
    if "access-control-allow-origin" in cors_headers:
        print(f"  ✅ Access-Control-Allow-Origin: {cors_headers['access-control-allow-origin']}")
    else:
        print(f"  ❌ Access-Control-Allow-Origin: Ausente")
    
    if "access-control-allow-methods" in cors_headers:
        print(f"  ✅ Access-Control-Allow-Methods: {cors_headers['access-control-allow-methods']}")
    else:
        print(f"  ℹ️  Access-Control-Allow-Methods: Ausente")

def test_rate_limiting():
    """Testa o rate limiting (10 req/s)"""
    print("\n⏱️  Testando Rate Limiting (10 req/s)...")
    
    # Fazer 15 requests rápidos para testar o limite
    success_count = 0
    rate_limited_count = 0
    
    start_time = time.time()
    
    for i in range(15):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"  ⚠️  Request {i+1}: Rate limited (429)")
        except requests.exceptions.Timeout:
            print(f"  ⏳ Request {i+1}: Timeout")
        except Exception as e:
            print(f"  ❌ Request {i+1}: Erro - {e}")
    
    elapsed_time = time.time() - start_time
    
    print(f"\n  📊 Resultados:")
    print(f"    - Requests bem-sucedidos: {success_count}")
    print(f"    - Requests limitados (429): {rate_limited_count}")
    print(f"    - Tempo total: {elapsed_time:.2f}s")
    print(f"    - Taxa: {15/elapsed_time:.2f} req/s")
    
    if rate_limited_count > 0:
        print(f"  ✅ Rate limiting funcionando!")
    else:
        print(f"  ⚠️  Nenhum request foi limitado (pode precisar de mais requests ou menor intervalo)")

def test_api_info():
    """Testa endpoint /info para verificar informações de segurança"""
    print("\n📋 Testando Endpoint /info...")
    
    response = requests.get(f"{BASE_URL}/info")
    
    if response.status_code == 200:
        data = response.json()
        
        if "security" in data:
            security = data["security"]
            print(f"  ✅ Informações de segurança presentes:")
            print(f"    - Rate limit (req/s): {security.get('rate_limit_per_second', 'N/A')}")
            print(f"    - Rate limit (req/min): {security.get('rate_limit_per_minute', 'N/A')}")
            print(f"    - Rate limit (req/hour): {security.get('rate_limit_per_hour', 'N/A')}")
            print(f"    - CORS origins: {security.get('cors_origins', 'N/A')}")
            print(f"    - HTTPS only: {security.get('https_only', 'N/A')}")
        else:
            print(f"  ❌ Informações de segurança ausentes")
    else:
        print(f"  ❌ Erro ao acessar /info: {response.status_code}")

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🔒 TESTE DE SEGURANÇA P3.2")
    print("Green Jobs Brasil - CORS, Rate Limiting e Security Headers")
    print("=" * 70)
    
    try:
        # Verificar se a API está rodando
        response = requests.get(f"{BASE_URL}/", timeout=2)
        print(f"\n✅ API acessível em {BASE_URL}")
        print(f"   Versão: {response.json().get('version', 'N/A')}")
    except Exception as e:
        print(f"\n❌ API não está acessível: {e}")
        print(f"   Certifique-se de que a API está rodando em {BASE_URL}")
        return
    
    # Executar testes
    test_security_headers()
    test_cors_headers()
    test_api_info()
    test_rate_limiting()
    
    print("\n" + "=" * 70)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 70)

if __name__ == "__main__":
    main()
