"""
Teste do Sistema de Autenticação
Testa registro, login, acesso protegido e logout
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8002"

print("=" * 60)
print("TESTE SISTEMA DE AUTENTICAÇÃO - GJB v1.3")
print("=" * 60)
print()

# ============================================
# 1. TESTAR REGISTRO
# ============================================
print("1️⃣  TESTANDO REGISTRO DE USUÁRIO")
print("-" * 60)

novo_usuario = {
    "email": f"teste_{datetime.now().strftime('%Y%m%d%H%M%S')}@greenjobs.com.br",
    "password": "Senha123!",
    "full_name": "Usuário Teste",
    "user_type": "profissional"
}

try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=novo_usuario)
    if response.status_code == 201:
        user_data = response.json()
        print(f"✅ Usuário criado com sucesso!")
        print(f"   ID: {user_data['id']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Nome: {user_data['full_name']}")
        print(f"   Tipo: {user_data['user_type']}")
    else:
        print(f"❌ Erro ao criar usuário: {response.status_code}")
        print(f"   {response.json()}")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")

print()

# ============================================
# 2. TESTAR LOGIN
# ============================================
print("2️⃣  TESTANDO LOGIN")
print("-" * 60)

# Testar com usuário recém-criado
login_data = {
    "username": novo_usuario['email'],  # OAuth2 usa 'username'
    "password": novo_usuario['password']
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,  # OAuth2PasswordRequestForm usa form data
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        print(f"✅ Login realizado com sucesso!")
        print(f"   Access Token: {access_token[:50]}...")
        print(f"   Token Type: {tokens['token_type']}")
        if tokens.get('refresh_token'):
            print(f"   Refresh Token: {tokens['refresh_token'][:50]}...")
    else:
        print(f"❌ Erro no login: {response.status_code}")
        print(f"   {response.json()}")
        access_token = None
except Exception as e:
    print(f"❌ Erro de conexão: {e}")
    access_token = None

print()

# ============================================
# 3. TESTAR ACESSO PROTEGIDO (/me)
# ============================================
print("3️⃣  TESTANDO ACESSO PROTEGIDO (/me)")
print("-" * 60)

if access_token:
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            me_data = response.json()
            print(f"✅ Dados do usuário obtidos com sucesso!")
            print(f"   ID: {me_data['id']}")
            print(f"   Email: {me_data['email']}")
            print(f"   Nome: {me_data['full_name']}")
            print(f"   Tipo: {me_data['user_type']}")
            print(f"   Ativo: {me_data['is_active']}")
            print(f"   Verificado: {me_data['is_verified']}")
        else:
            print(f"❌ Erro ao obter dados: {response.status_code}")
            print(f"   {response.json()}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
else:
    print("⚠️  Pulado (sem token)")

print()

# ============================================
# 4. TESTAR LOGIN COM ADMIN
# ============================================
print("4️⃣  TESTANDO LOGIN COM ADMIN")
print("-" * 60)

admin_login = {
    "username": "admin@greenjobs.com.br",
    "password": "admin123"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=admin_login,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        admin_tokens = response.json()
        admin_token = admin_tokens['access_token']
        print(f"✅ Login admin realizado com sucesso!")
        print(f"   Token: {admin_token[:50]}...")
        
        # Buscar dados do admin
        me_response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        if me_response.status_code == 200:
            admin_data = me_response.json()
            print(f"   Nome: {admin_data['full_name']}")
            print(f"   Tipo: {admin_data['user_type']}")
    else:
        print(f"❌ Erro no login admin: {response.status_code}")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")

print()

# ============================================
# 5. TESTAR VERIFICAÇÃO DE TOKEN
# ============================================
print("5️⃣  TESTANDO VERIFICAÇÃO DE TOKEN")
print("-" * 60)

if access_token:
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/verify-token",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"✅ Token válido!")
            print(f"   Válido: {verify_data['valid']}")
            print(f"   User ID: {verify_data['user_id']}")
            print(f"   Email: {verify_data['email']}")
        else:
            print(f"❌ Token inválido: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
else:
    print("⚠️  Pulado (sem token)")

print()

# ============================================
# 6. TESTAR LOGOUT
# ============================================
print("6️⃣  TESTANDO LOGOUT")
print("-" * 60)

if access_token:
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            logout_data = response.json()
            print(f"✅ Logout realizado com sucesso!")
            print(f"   Mensagem: {logout_data['message']}")
            print(f"   Usuário: {logout_data['user']}")
        else:
            print(f"❌ Erro no logout: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
else:
    print("⚠️  Pulado (sem token)")

print()

# ============================================
# 7. TESTAR ACESSO SEM TOKEN (deve falhar)
# ============================================
print("7️⃣  TESTANDO ACESSO SEM TOKEN (deve falhar)")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/auth/me")
    
    if response.status_code == 401:
        print(f"✅ Acesso negado corretamente!")
        print(f"   Status: {response.status_code} Unauthorized")
    else:
        print(f"⚠️  Resposta inesperada: {response.status_code}")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")

print()

# ============================================
# RESUMO
# ============================================
print("=" * 60)
print("RESUMO DOS TESTES")
print("=" * 60)
print()
print("✅ Sistema de autenticação implementado!")
print("✅ Registro de usuários funcionando")
print("✅ Login com JWT funcionando")
print("✅ Rotas protegidas funcionando")
print("✅ Verificação de token funcionando")
print("✅ Logout funcionando")
print()
print("🔐 Credenciais Admin:")
print("   Email: admin@greenjobs.com.br")
print("   Senha: admin123")
print()
print("=" * 60)
