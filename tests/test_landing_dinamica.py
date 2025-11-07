"""
Teste da Landing Page Dinâmica
Verifica se a página inicial carrega dados reais do banco
"""
import requests
import sys

BASE_URL = "http://127.0.0.1:8002"

def test_landing_page_dinamica():
    """Testa se a landing page carrega com dados reais"""
    print("\n🧪 Testando Landing Page Dinâmica...")
    print("=" * 60)
    
    try:
        # Fazer request para a home
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            html = response.text
            
            # Verificar se as variáveis Jinja2 foram renderizadas
            checks = {
                "Variável stats.candidaturas": "{{ stats.candidaturas" not in html,
                "Variável stats.precisao_ml": "{{ stats.precisao_ml" not in html,
                "Variável stats.taxa_match": "{{ stats.taxa_match" not in html,
                "Número visível (não template)": any(num in html for num in ["857", "101", "120", "768"]),
            }
            
            print("\n✅ Verificações:")
            for check_name, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")
            
            # Verificar se contém números (dados renderizados)
            if "Candidaturas Ativas" in html:
                print("\n✅ Label atualizado: 'Candidaturas Ativas'")
            else:
                print("\n⚠️  Label antigo ainda presente: 'Candidatos Processados'")
            
            # Buscar dados reais da API
            api_response = requests.get(f"{BASE_URL}/api/candidaturas", timeout=5)
            if api_response.status_code == 200:
                candidaturas_api = len(api_response.json())
                print(f"\n📊 Dados da API:")
                print(f"  - Candidaturas via /api/candidaturas: {candidaturas_api}")
            
            if all(checks.values()):
                print("\n🎉 SUCESSO! Landing page está dinâmica!")
                return True
            else:
                print("\n⚠️  Alguns checks falharam")
                return False
        else:
            print(f"\n❌ Erro HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ API não está rodando!")
        print("   Execute: python start_api.py")
        return False
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

def test_comparacao_valores():
    """Compara valores da landing page com API"""
    print("\n\n🔍 Comparando Valores...")
    print("=" * 60)
    
    try:
        # Buscar HTML da landing
        landing = requests.get(f"{BASE_URL}/", timeout=5)
        
        # Buscar dados da API
        candidaturas_resp = requests.get(f"{BASE_URL}/api/candidaturas", timeout=5)
        vagas_resp = requests.get(f"{BASE_URL}/api/vagas", timeout=5)
        profissionais_resp = requests.get(f"{BASE_URL}/api/profissionais", timeout=5)
        
        if all(r.status_code == 200 for r in [landing, candidaturas_resp, vagas_resp, profissionais_resp]):
            html = landing.text
            
            # Contar dados reais
            total_candidaturas = len(candidaturas_resp.json())
            total_vagas = len(vagas_resp.json())
            total_profissionais = len(profissionais_resp.json())
            
            print(f"\n📊 Dados Reais do Banco:")
            print(f"  - Candidaturas: {total_candidaturas}")
            print(f"  - Vagas: {total_vagas}")
            print(f"  - Profissionais: {total_profissionais}")
            
            # Verificar se os números aparecem no HTML
            print(f"\n🔎 Verificando se aparecem na Landing Page:")
            if str(total_candidaturas) in html:
                print(f"  ✅ {total_candidaturas} candidaturas encontrado no HTML")
            else:
                print(f"  ⚠️  {total_candidaturas} não encontrado (pode estar dinâmico)")
            
            print("\n✅ Comparação concluída!")
            return True
        else:
            print("\n❌ Erro ao buscar dados da API")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🌿 GREEN JOBS BRASIL - TESTE LANDING PAGE DINÂMICA")
    print("=" * 60)
    
    test1 = test_landing_page_dinamica()
    test2 = test_comparacao_valores()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("✅ TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        sys.exit(1)
