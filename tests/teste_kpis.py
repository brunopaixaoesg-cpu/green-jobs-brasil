"""
Teste do endpoint de KPIs consolidados
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def test_kpis_gerais():
    """Testar KPIs gerais"""
    print("\n" + "="*50)
    print("TESTANDO: /api/kpis/gerais")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/api/kpis/gerais")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ KPIs Gerais:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {response.text}")

def test_kpis_consolidados():
    """Testar KPIs consolidados"""
    print("\n" + "="*50)
    print("TESTANDO: /api/kpis/ (consolidados)")
    print("="*50)
    
    # Teste 1: Por mês (padrão)
    print("\n📊 Tendências mensais:")
    response = requests.get(f"{BASE_URL}/api/kpis/", params={"periodo": "mes", "limit_top": 5})
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n📈 Métricas Gerais:")
        for key, value in data["gerais"].items():
            print(f"  {key}: {value}")
        
        print(f"\n📅 Tendências (últimos {len(data['tendencias'])} meses):")
        for t in data["tendencias"][-5:]:  # Últimos 5
            print(f"  {t['periodo']}: {t['novos_profissionais']} profissionais, {t['novas_vagas']} vagas")
        
        print(f"\n🏆 Top 5 Profissionais:")
        for p in data["top_profissionais"]:
            print(f"  {p['nome']}: {int(p['valor'])} {p['metrica']}")
        
        print(f"\n🏢 Top 5 Empresas:")
        for e in data["top_empresas"]:
            print(f"  {e['nome']}: {int(e['valor'])} {e['metrica']}")
        
        print(f"\n💼 Top 5 Vagas:")
        for v in data["top_vagas"]:
            print(f"  {v['nome']}: {int(v['valor'])} {v['metrica']}")
        
        print(f"\n🎯 ODS Mais Buscados:")
        for ods in data["ods_mais_buscados"]:
            print(f"  ODS {ods['ods']}: {ods['count']} menções")
        
        print(f"\n💡 Áreas Mais Demandadas:")
        for area in data["areas_mais_demandadas"]:
            print(f"  {area['area']}: {area['count']} vagas")
    else:
        print(f"❌ Erro: {response.text}")
    
    # Teste 2: Por semana
    print("\n📊 Tendências semanais (últimas 4 semanas):")
    response = requests.get(f"{BASE_URL}/api/kpis/", params={"periodo": "semana", "limit_top": 3})
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        for t in data["tendencias"][-4:]:
            print(f"  {t['periodo']}: {t['novas_candidaturas']} candidaturas, {t['matches_realizados']} matches")

def test_performance():
    """Testar performance"""
    import time
    
    print("\n" + "="*50)
    print("TESTE DE PERFORMANCE")
    print("="*50)
    
    # KPIs gerais (endpoint rápido)
    start = time.time()
    response = requests.get(f"{BASE_URL}/api/kpis/gerais")
    elapsed_gerais = time.time() - start
    print(f"\n⚡ /api/kpis/gerais: {elapsed_gerais:.3f}s")
    
    # KPIs consolidados
    start = time.time()
    response = requests.get(f"{BASE_URL}/api/kpis/")
    elapsed_consolidados = time.time() - start
    print(f"⚡ /api/kpis/ (consolidados): {elapsed_consolidados:.3f}s")
    
    if elapsed_consolidados < 2.0:
        print("✅ Performance OK (< 2s)")
    else:
        print("⚠️ Performance pode ser melhorada (considere cache)")

if __name__ == "__main__":
    print("\n🚀 Iniciando testes do endpoint /api/kpis")
    
    try:
        test_kpis_gerais()
        test_kpis_consolidados()
        test_performance()
        
        print("\n" + "="*50)
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: API não está rodando em http://127.0.0.1:8002")
        print("Execute: python start_api.py")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
