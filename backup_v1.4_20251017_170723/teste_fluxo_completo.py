"""
Teste Completo do Fluxo de Autenticação
Login → Dashboard → Dados do Usuário
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print("=" * 70)
print("TESTE COMPLETO - FLUXO DE AUTENTICAÇÃO")
print("=" * 70)
print()

# Credenciais
EMAIL = "bruno@greenjobsbrasil.com.br"
PASSWORD = "Senha123!"

print(f"📧 Testando com: {EMAIL}")
print("-" * 70)
print()

# 1. LOGIN
print("1️⃣  FAZENDO LOGIN...")
try:
    login_data = {
        "username": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        print(f"✅ Login bem-sucedido!")
        print(f"   Token: {access_token[:50]}...")
    else:
        print(f"❌ Erro no login: {response.status_code}")
        print(f"   {response.json()}")
        exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)

print()

# 2. BUSCAR DADOS DO USUÁRIO
print("2️⃣  BUSCANDO DADOS DO USUÁRIO...")
try:
    response = requests.get(
        f"{BASE_URL}/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Dados obtidos com sucesso!")
        print(f"   ID: {user['id']}")
        print(f"   Nome: {user['full_name']}")
        print(f"   Email: {user['email']}")
        print(f"   Tipo: {user['user_type']}")
        print(f"   Ativo: {user['is_active']}")
        print(f"   Verificado: {user['is_verified']}")
    else:
        print(f"❌ Erro ao buscar dados: {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 3. ACESSAR DASHBOARD
print("3️⃣  ACESSANDO DASHBOARD...")
try:
    response = requests.get(f"{BASE_URL}/dashboard")
    if response.status_code == 200:
        print(f"✅ Dashboard acessível!")
        print(f"   Status: {response.status_code}")
        print(f"   Tamanho: {len(response.text)} bytes")
    else:
        print(f"❌ Erro ao acessar dashboard: {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 4. BUSCAR ESTATÍSTICAS
print("4️⃣  BUSCANDO ESTATÍSTICAS DO SISTEMA...")
try:
    response = requests.get(f"{BASE_URL}/api/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Estatísticas obtidas!")
        print(f"   Empresas: {stats.get('total_empresas', 0)}")
        print(f"   Vagas: {stats.get('total_vagas', 0)}")
        print(f"   Profissionais: {stats.get('total_profissionais', 0)}")
        print(f"   Score Médio: {stats.get('score_medio_empresas', 0):.1f}%")
    else:
        print(f"⚠️  Stats não disponíveis: {response.status_code}")
except Exception as e:
    print(f"⚠️  Erro ao buscar stats: {e}")

print()

# 5. BUSCAR MATCHING
print("5️⃣  BUSCANDO ESTATÍSTICAS DE MATCHING...")
try:
    response = requests.get(f"{BASE_URL}/api/matching/stats")
    if response.status_code == 200:
        matching = response.json()
        print(f"✅ Matching stats obtidas!")
        print(f"   Candidaturas: {matching.get('total_candidaturas', 0)}")
        print(f"   Score Médio: {matching.get('score_medio', 0):.1f}%")
        print(f"   Matches ≥80%: {matching.get('matches_excelentes', 0)}")
    else:
        print(f"⚠️  Matching stats não disponíveis: {response.status_code}")
except Exception as e:
    print(f"⚠️  Erro ao buscar matching: {e}")

print()

# 6. VERIFICAR TOKEN
print("6️⃣  VERIFICANDO VALIDADE DO TOKEN...")
try:
    response = requests.get(
        f"{BASE_URL}/api/auth/verify-token",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if response.status_code == 200:
        verify = response.json()
        print(f"✅ Token válido!")
        print(f"   User ID: {verify['user_id']}")
        print(f"   Email: {verify['email']}")
    else:
        print(f"❌ Token inválido: {response.status_code}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 7. TESTAR PÁGINAS PRINCIPAIS
print("7️⃣  TESTANDO ACESSO ÀS PÁGINAS...")
pages = [
    ("/", "Home"),
    ("/dashboard", "Dashboard"),
    ("/empresas", "Empresas"),
    ("/vagas", "Vagas"),
    ("/profissionais", "Profissionais"),
    ("/ml-avancado", "ML Dashboard"),
]

for path, name in pages:
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=3)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"   {status} {name}: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {name}: ERRO")

print()
print("=" * 70)
print("TESTE COMPLETO FINALIZADO!")
print("=" * 70)
print()
print("🌐 ACESSE AS PÁGINAS:")
print(f"   Login: {BASE_URL}/login")
print(f"   Dashboard: {BASE_URL}/dashboard")
print()
print("📝 SUAS CREDENCIAIS:")
print(f"   Email: {EMAIL}")
print(f"   Senha: {PASSWORD}")
print()
print("=" * 70)
