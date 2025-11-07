"""
Teste Simples para Health Check Endpoints - P3.4
Testa diretamente os endpoints sem importar o app
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time

BASE_URL = "http://127.0.0.1:8002"

def test_health():
    """Testa endpoint /health"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: GET /health")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    print(f"Response: {data}")
    
    # Validar estrutura
    assert "status" in data
    assert "database" in data
    assert "version" in data
    
    print(f"✅ Status: {data['status']}")
    print(f"✅ DB Connected: {data['database']['connected']}")
    print(f"✅ DB Response Time: {data['database']['response_time_ms']}ms")
    
def test_ready():
    """Testa endpoint /ready"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: GET /ready")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/ready")
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    print(f"Response: {data}")
    
    # Validar estrutura
    assert "ready" in data
    assert "checks" in data
    
    print(f"✅ Ready: {data['ready']}")
    print(f"✅ Checks:")
    for check, status in data['checks'].items():
        print(f"   - {check}: {status}")

def test_metrics_prometheus():
    """Testa endpoint /metrics"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: GET /metrics (Prometheus format)")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/metrics")
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "text/plain" in response.headers.get('content-type', ''), "Should be text/plain"
    
    content = response.text
    lines = content.split("\n")
    
    print(f"Total lines: {len(lines)}")
    print(f"Sample metrics:")
    for line in lines[:10]:
        if line and not line.startswith("#"):
            print(f"   {line}")
    
    # Validar métricas importantes
    assert "greenjobs_db_health" in content
    assert "greenjobs_uptime_seconds" in content
    print(f"✅ Prometheus metrics OK")

def test_metrics_json():
    """Testa endpoint /metrics/json"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: GET /metrics/json")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/metrics/json")
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Validar estrutura
    assert "system" in data
    assert "database" in data
    assert "api" in data
    
    print(f"✅ System Memory: {data['system']['memory_mb']} MB")
    print(f"✅ System CPU: {data['system']['cpu_percent']}%")
    print(f"✅ DB Empresas: {data['database']['empresas_total']}")
    print(f"✅ DB Profissionais: {data['database']['profissionais_total']}")
    print(f"✅ API Version: {data['api']['version']}")
    print(f"✅ API Uptime: {data['api']['uptime_seconds']}s")

def test_performance():
    """Testa performance"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Performance")
    print("=" * 60)
    
    endpoints = [
        "/health",
        "/ready",
        "/metrics",
        "/metrics/json"
    ]
    
    for endpoint in endpoints:
        start = time.time()
        response = requests.get(f"{BASE_URL}{endpoint}")
        duration_ms = (time.time() - start) * 1000
        
        status = "✅" if response.status_code == 200 else "❌"
        perf = "✅" if duration_ms < 500 else "⚠️"
        
        print(f"{status} {perf} {endpoint}: {duration_ms:.2f}ms")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 TESTES DE HEALTH CHECKS (P3.4)")
    print("=" * 60)
    print(f"⚠️  Certifique-se de que a API está rodando em {BASE_URL}")
    print("=" * 60)
    
    try:
        # Verificar se API está online
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
        except requests.exceptions.RequestException:
            print(f"\n❌ API não está acessível em {BASE_URL}")
            print("   Execute: python start_api.py")
            sys.exit(1)
        
        test_health()
        test_ready()
        test_metrics_prometheus()
        test_metrics_json()
        test_performance()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
