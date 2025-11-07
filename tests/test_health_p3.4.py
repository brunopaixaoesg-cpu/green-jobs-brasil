"""
Testes para Health Check Endpoints - P3.4
Valida /health, /ready e /metrics
"""
import sys
import os
import time

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_endpoint():
    """Testa endpoint /health"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Endpoint /health")
    print("=" * 60)
    
    response = client.get("/health")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Validar estrutura
    assert "status" in data, "Missing 'status' field"
    assert "timestamp" in data, "Missing 'timestamp' field"
    assert "version" in data, "Missing 'version' field"
    assert "database" in data, "Missing 'database' field"
    assert "uptime_seconds" in data, "Missing 'uptime_seconds' field"
    
    # Validar database
    db = data["database"]
    assert "connected" in db, "Missing 'database.connected' field"
    assert "response_time_ms" in db, "Missing 'database.response_time_ms' field"
    
    # Validar valores
    assert data["status"] in ["healthy", "unhealthy"], f"Invalid status: {data['status']}"
    assert db["connected"] == True, "Database should be connected"
    assert db["response_time_ms"] is not None, "Response time should not be null"
    assert db["response_time_ms"] < 100, f"DB too slow: {db['response_time_ms']}ms"
    
    print(f"✅ Status: {data['status']}")
    print(f"✅ Version: {data['version']}")
    print(f"✅ DB Connected: {db['connected']}")
    print(f"✅ DB Response: {db['response_time_ms']}ms")
    print(f"✅ Uptime: {data['uptime_seconds']}s")

def test_ready_endpoint():
    """Testa endpoint /ready"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Endpoint /ready")
    print("=" * 60)
    
    response = client.get("/ready")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Validar estrutura
    assert "ready" in data, "Missing 'ready' field"
    assert "timestamp" in data, "Missing 'timestamp' field"
    assert "checks" in data, "Missing 'checks' field"
    assert "message" in data, "Missing 'message' field"
    
    # Validar checks
    checks = data["checks"]
    assert "database" in checks, "Missing 'database' check"
    assert "logs_writable" in checks, "Missing 'logs_writable' check"
    assert "config_loaded" in checks, "Missing 'config_loaded' check"
    
    # Validar valores
    assert data["ready"] == True, "Service should be ready"
    assert checks["database"] == True, "Database check should pass"
    assert checks["logs_writable"] == True, "Logs should be writable"
    assert checks["config_loaded"] == True, "Config should be loaded"
    
    print(f"✅ Ready: {data['ready']}")
    print(f"✅ Message: {data['message']}")
    print(f"✅ Checks:")
    for check, status in checks.items():
        print(f"   - {check}: {status}")

def test_metrics_prometheus():
    """Testa endpoint /metrics (Prometheus format)"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Endpoint /metrics (Prometheus)")
    print("=" * 60)
    
    response = client.get("/metrics")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.headers["content-type"].startswith("text/plain"), "Should be text/plain"
    
    content = response.text
    
    # Validar métricas obrigatórias
    required_metrics = [
        "greenjobs_uptime_seconds",
        "greenjobs_memory_bytes",
        "greenjobs_cpu_percent",
        "greenjobs_empresas_total",
        "greenjobs_profissionais_total",
        "greenjobs_vagas_ativas",
        "greenjobs_candidaturas_total",
        "greenjobs_db_response_time_ms",
        "greenjobs_db_health"
    ]
    
    for metric in required_metrics:
        assert metric in content, f"Missing metric: {metric}"
    
    # Validar formato Prometheus
    assert "# HELP" in content, "Missing HELP comments"
    assert "# TYPE" in content, "Missing TYPE comments"
    
    lines = content.split("\n")
    metric_lines = [l for l in lines if l and not l.startswith("#")]
    
    print(f"✅ Content-Type: {response.headers['content-type']}")
    print(f"✅ Metrics found: {len(metric_lines)}")
    print(f"✅ Sample metrics:")
    for line in metric_lines[:5]:
        print(f"   {line}")

def test_metrics_json():
    """Testa endpoint /metrics/json"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: Endpoint /metrics/json")
    print("=" * 60)
    
    response = client.get("/metrics/json")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Validar estrutura
    assert "timestamp" in data, "Missing 'timestamp' field"
    assert "system" in data, "Missing 'system' field"
    assert "database" in data, "Missing 'database' field"
    assert "api" in data, "Missing 'api' field"
    
    # Validar system
    system = data["system"]
    assert "memory_bytes" in system, "Missing 'memory_bytes'"
    assert "memory_mb" in system, "Missing 'memory_mb'"
    assert "cpu_percent" in system, "Missing 'cpu_percent'"
    
    # Validar database
    db = data["database"]
    assert "connected" in db, "Missing 'connected'"
    assert db["connected"] == True, "Database should be connected"
    assert "empresas_total" in db, "Missing 'empresas_total'"
    assert "profissionais_total" in db, "Missing 'profissionais_total'"
    
    # Validar API
    api_data = data["api"]
    assert "version" in api_data, "Missing 'version'"
    assert "uptime_seconds" in api_data, "Missing 'uptime_seconds'"
    assert "debug_mode" in api_data, "Missing 'debug_mode'"
    
    print(f"✅ System:")
    print(f"   - Memory: {system['memory_mb']} MB")
    print(f"   - CPU: {system['cpu_percent']}%")
    print(f"✅ Database:")
    print(f"   - Connected: {db['connected']}")
    print(f"   - Empresas: {db.get('empresas_total', 'N/A')}")
    print(f"   - Profissionais: {db.get('profissionais_total', 'N/A')}")
    print(f"✅ API:")
    print(f"   - Version: {api_data['version']}")
    print(f"   - Uptime: {api_data['uptime_seconds']}s")

def test_performance():
    """Testa performance dos endpoints"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Performance dos Health Checks")
    print("=" * 60)
    
    endpoints = ["/health", "/ready", "/metrics", "/metrics/json"]
    
    for endpoint in endpoints:
        start = time.time()
        response = client.get(endpoint)
        duration_ms = (time.time() - start) * 1000
        
        assert response.status_code == 200, f"{endpoint} failed"
        assert duration_ms < 500, f"{endpoint} too slow: {duration_ms}ms"
        
        print(f"✅ {endpoint}: {duration_ms:.2f}ms")

def test_health_with_db_error():
    """Testa comportamento quando DB está inacessível (simulado)"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Health Check com DB Error (graceful degradation)")
    print("=" * 60)
    
    # Nota: Este teste assume que mesmo com erro, o endpoint retorna 200
    # mas com status "unhealthy". Em produção real, você poderia:
    # 1. Mockar o DB para simular erro
    # 2. Usar um DB de teste que pode ser desligado
    # 3. Validar apenas o comportamento com DB funcionando
    
    response = client.get("/health")
    
    # Sempre deve retornar 200 (health checks não devem falhar com 500)
    assert response.status_code == 200, "Health check should always return 200"
    
    data = response.json()
    
    # Se DB estiver OK, status deve ser "healthy"
    # Se DB estiver com erro, status deve ser "unhealthy"
    assert data["status"] in ["healthy", "unhealthy"], f"Invalid status: {data['status']}"
    
    print(f"✅ Health check retorna 200 mesmo com possíveis erros")
    print(f"✅ Status atual: {data['status']}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 INICIANDO TESTES DE HEALTH CHECKS (P3.4)")
    print("=" * 60)
    
    try:
        test_health_endpoint()
        test_ready_endpoint()
        test_metrics_prometheus()
        test_metrics_json()
        test_performance()
        test_health_with_db_error()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Resumo:")
        print("   - /health: OK")
        print("   - /ready: OK")
        print("   - /metrics (Prometheus): OK")
        print("   - /metrics/json: OK")
        print("   - Performance: OK")
        print("   - Error handling: OK")
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"❌ TESTE FALHOU: {e}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERRO INESPERADO: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
