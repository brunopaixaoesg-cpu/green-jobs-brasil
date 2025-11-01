"""Script para testar a integração com a Receita Federal na página de empresas"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print("🧪 TESTANDO INTEGRAÇÃO COM RECEITA FEDERAL\n")
print("=" * 60)

# Teste 1: Buscar empresa na Receita
print("\n✅ Teste 1: Buscar empresa por CNPJ")
cnpj_teste = "60331021000111"
print(f"   CNPJ: {cnpj_teste}")

try:
    response = requests.get(f"{BASE_URL}/api/search-company/{cnpj_teste}", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Status: {response.status_code} OK")
        print(f"   📊 Nome: {data.get('nome', 'N/A')}")
        print(f"   🎯 Score Verde: {data.get('green_score', 0)}/100")
        print(f"   🏷️  É Verde: {'Sim' if data.get('is_green') else 'Não'}")
        print(f"   📍 Localização: {data.get('municipio', 'N/A')}/{data.get('uf', 'N/A')}")
        print(f"   🏭 Situação: {data.get('situacao', 'N/A')}")
        
        cnaes = data.get('cnaes', [])
        if cnaes:
            print(f"   📋 CNAEs: {', '.join(cnaes[:3])}...")
        
        print("\n   ✅ Endpoint de busca funcionando corretamente!")
    else:
        print(f"   ❌ Erro: Status {response.status_code}")
        print(f"   Detalhes: {response.text}")
except Exception as e:
    print(f"   ❌ Erro na requisição: {e}")

# Teste 2: Verificar página de empresas
print("\n✅ Teste 2: Verificar página de empresas")
try:
    response = requests.get(f"{BASE_URL}/empresas", timeout=5)
    
    if response.status_code == 200:
        print(f"   ✓ Status: {response.status_code} OK")
        print(f"   ✓ Página carregada com sucesso")
        
        # Verificar se tem os elementos esperados
        html = response.text
        if 'buscarNaReceita' in html:
            print("   ✓ Função buscarNaReceita() presente")
        if 'receita-btn' in html:
            print("   ✓ Botão de busca presente")
        if 'receita-result' in html:
            print("   ✓ Container de resultado presente")
        
        print("\n   ✅ Página de empresas funcionando corretamente!")
    else:
        print(f"   ❌ Erro: Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro na requisição: {e}")

# Teste 3: Listar empresas cadastradas
print("\n✅ Teste 3: Listar empresas cadastradas")
try:
    response = requests.get(f"{BASE_URL}/api/empresas", timeout=5)
    
    if response.status_code == 200:
        empresas = response.json()
        print(f"   ✓ Status: {response.status_code} OK")
        print(f"   📊 Total de empresas: {len(empresas)}")
        
        if len(empresas) > 0:
            print(f"\n   📋 Primeiras empresas:")
            for i, emp in enumerate(empresas[:3], 1):
                print(f"      {i}. {emp.get('razao_social', 'N/A')} - Score: {emp.get('green_score', 0)}")
        
        print("\n   ✅ API de listagem funcionando corretamente!")
    else:
        print(f"   ❌ Erro: Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro na requisição: {e}")

print("\n" + "=" * 60)
print("\n✅ TESTES CONCLUÍDOS!")
print("\n🌐 Acesse a página para testar manualmente:")
print(f"   {BASE_URL}/empresas")
print("\n💡 Digite um CNPJ e clique em 'Buscar CNPJ na Receita'")
print("   Exemplo de CNPJ: 60.331.021/0001-11 ou 60331021000111\n")
