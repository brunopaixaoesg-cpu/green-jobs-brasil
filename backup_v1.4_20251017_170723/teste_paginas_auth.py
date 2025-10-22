"""
Teste das Páginas de Autenticação
Verifica se login e registro estão acessíveis
"""
import requests

BASE_URL = "http://127.0.0.1:8002"

print("=" * 60)
print("TESTE PÁGINAS DE AUTENTICAÇÃO - GJB v1.3")
print("=" * 60)
print()

# Testar páginas HTML
pages = [
    ("/", "Landing Page"),
    ("/dashboard", "Dashboard Principal"),
    ("/login", "Página de Login"),
    ("/registro", "Página de Registro"),
    ("/ml-avancado", "Dashboard ML"),
    ("/empresas", "Página de Empresas"),
    ("/vagas", "Página de Vagas"),
    ("/profissionais", "Página de Profissionais")
]

print("📄 TESTANDO PÁGINAS HTML:")
print("-" * 60)

for path, name in pages:
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=5)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {name}: {response.status_code}")
    except Exception as e:
        print(f"❌ {name}: ERRO - {str(e)[:50]}")

print()
print("=" * 60)

# Testar endpoints de API
api_endpoints = [
    ("/api/auth/me", "GET", "Perfil do Usuário (sem auth)"),
    ("/api/stats", "GET", "Estatísticas"),
    ("/api/empresas", "GET", "Lista de Empresas"),
    ("/api/vagas", "GET", "Lista de Vagas"),
]

print("🔌 TESTANDO ENDPOINTS DE API:")
print("-" * 60)

for path, method, name in api_endpoints:
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
        
        # 401 é esperado para rotas protegidas
        if path == "/api/auth/me" and response.status_code == 401:
            print(f"✅ {name}: {response.status_code} (Proteção OK)")
        elif response.status_code == 200:
            print(f"✅ {name}: {response.status_code}")
        else:
            print(f"⚠️ {name}: {response.status_code}")
    except Exception as e:
        print(f"❌ {name}: ERRO - {str(e)[:50]}")

print()
print("=" * 60)
print("ACESSE AS PÁGINAS:")
print("=" * 60)
print(f"🔐 Login: {BASE_URL}/login")
print(f"📝 Registro: {BASE_URL}/registro")
print(f"🏠 Home: {BASE_URL}/")
print(f"📊 Dashboard: {BASE_URL}/dashboard")
print("=" * 60)
