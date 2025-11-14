"""
Script de teste rápido da API - Green Jobs Brasil
Testa endpoints principais e TSB
"""
import requests
import sys

BASE_URL = "http://127.0.0.1:8002"

def test_endpoint(name, url, expected_status=200):
    """Testa um endpoint e retorna resultado"""
    try:
        response = requests.get(url, timeout=5)
        success = response.status_code == expected_status
        
        if success:
            print(f"✅ {name}: OK ({response.status_code})")
            return True
        else:
            print(f"❌ {name}: FALHOU ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: ERRO - {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTE RÁPIDO - GREEN JOBS BRASIL API")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_total = 0
    
    # Testes básicos
    print("📋 ENDPOINTS BÁSICOS")
    print("-" * 60)
    
    tests_total += 1
    if test_endpoint("Health Check", f"{BASE_URL}/health"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("Documentação Swagger", f"{BASE_URL}/docs"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("Stats Gerais", f"{BASE_URL}/api/stats"):
        tests_passed += 1
    
    print()
    
    # Testes TSB
    print("🌱 ENDPOINTS TSB")
    print("-" * 60)
    
    tests_total += 1
    if test_endpoint("TSB Objetivos", f"{BASE_URL}/api/taxonomia/objetivos"):
        tests_passed += 1
        try:
            r = requests.get(f"{BASE_URL}/api/taxonomia/objetivos", timeout=5)
            data = r.json()
            print(f"   → {len(data)} objetivos carregados")
        except:
            pass
    
    tests_total += 1
    if test_endpoint("TSB Setores", f"{BASE_URL}/api/taxonomia/setores"):
        tests_passed += 1
        try:
            r = requests.get(f"{BASE_URL}/api/taxonomia/setores", timeout=5)
            data = r.json()
            print(f"   → {len(data)} setores carregados")
        except:
            pass
    
    tests_total += 1
    if test_endpoint("TSB Critérios", f"{BASE_URL}/api/taxonomia/criterios"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("TSB Info", f"{BASE_URL}/api/taxonomia/info"):
        tests_passed += 1
    
    print()
    
    # Testes de empresas
    print("🏢 ENDPOINTS EMPRESAS")
    print("-" * 60)
    
    tests_total += 1
    if test_endpoint("Listar Empresas", f"{BASE_URL}/api/empresas"):
        tests_passed += 1
    
    tests_total += 1
    if test_endpoint("Empresas com TSB", f"{BASE_URL}/api/empresas?tsb=true"):
        tests_passed += 1
        try:
            r = requests.get(f"{BASE_URL}/api/empresas?tsb=true", timeout=5)
            data = r.json()
            if len(data) > 0:
                empresa = data[0]
                if 'tsb_elegivel' in empresa:
                    print(f"   → Enriquecimento TSB: ✅")
                    print(f"   → TSB Elegível: {empresa.get('tsb_elegivel')}")
                    print(f"   → TSB Score: {empresa.get('tsb_score')}")
                else:
                    print(f"   → Enriquecimento TSB: ❌")
        except:
            pass
    
    print()
    
    # Resultado final
    print("=" * 60)
    print(f"📊 RESULTADO: {tests_passed}/{tests_total} testes passaram")
    print("=" * 60)
    
    if tests_passed == tests_total:
        print("✅ TODOS OS TESTES PASSARAM!")
        print()
        print("🎯 Próximos passos:")
        print("   1. Acesse: http://127.0.0.1:8002/docs")
        print("   2. Explore os endpoints TSB")
        print("   3. Teste empresas com enriquecimento TSB")
        return 0
    else:
        print(f"⚠️  {tests_total - tests_passed} teste(s) falharam")
        print()
        print("💡 Dicas:")
        print("   - Verifique se a API está rodando")
        print("   - Execute: python start_api.py")
        print("   - Aguarde a API inicializar completamente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
