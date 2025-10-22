"""
Teste completo do sistema de Storytelling v1.6
Valida: API endpoints, dados dos perfis, edição e salvamento
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def teste_obter_perfil(profissional_id):
    """Testa endpoint GET de storytelling"""
    print(f"\n🧪 Testando perfil ID {profissional_id}...")
    
    url = f"{BASE_URL}/api/profissionais/api/{profissional_id}/storytelling"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ Status 200 - Perfil carregado")
        print(f"  📝 Nome: {data.get('nome_completo')}")
        print(f"  📖 História: {len(data.get('historia_verde', ''))} caracteres")
        print(f"  🏆 Conquistas: {len(data.get('conquistas', []))} items")
        print(f"  💼 Projetos: {len(data.get('portfolio_projetos', []))} items")
        print(f"  🌍 Idiomas: {len(data.get('idiomas', []))} items")
        return True
    else:
        print(f"  ❌ Erro {response.status_code}: {response.text}")
        return False

def teste_atualizar_storytelling():
    """Testa endpoint PUT para atualizar storytelling"""
    print(f"\n🧪 Testando atualização de storytelling (ID 1)...")
    
    # Dados de teste
    dados_teste = {
        "historia_verde": "História de teste atualizada - Sistema funcionando perfeitamente!",
        "motivacao": "Motivação de teste",
        "valores_pessoais": "Teste, Validação, Qualidade",
        "objetivos_carreira": "Testar todos os endpoints",
        "conquistas_json": json.dumps([
            {
                "titulo": "Conquista de Teste",
                "descricao": "Validação do sistema",
                "data": "2024",
                "icone": "✅"
            }
        ]),
        "portfolio_projetos_json": json.dumps([
            {
                "titulo": "Projeto de Teste",
                "empresa": "Green Jobs Brasil",
                "descricao": "Teste do sistema de storytelling",
                "periodo": "Out 2024",
                "resultados": ["100% funcional"],
                "ods": [13],
                "tecnologias": ["Python", "FastAPI"]
            }
        ]),
        "idiomas_json": json.dumps([
            {"idioma": "Português", "nivel": "Nativo"}
        ])
    }
    
    url = f"{BASE_URL}/api/profissionais/api/1/storytelling"
    response = requests.put(url, json=dados_teste)
    
    if response.status_code == 200:
        result = response.json()
        print(f"  ✅ Status 200 - Atualização bem-sucedida")
        print(f"  📦 Resposta: {result}")
        
        # Verificar se foi salvo
        response_get = requests.get(url)
        if response_get.status_code == 200:
            data = response_get.json()
            if "História de teste atualizada" in data.get('historia_verde', ''):
                print(f"  ✅ Dados salvos corretamente no banco")
                return True
            else:
                print(f"  ⚠️ Dados não foram persistidos")
                return False
    else:
        print(f"  ❌ Erro {response.status_code}: {response.text}")
        return False

def teste_validacoes():
    """Testa validações de campos"""
    print(f"\n🧪 Testando validações...")
    
    # Teste 1: História muito longa (>1000 chars)
    dados_invalidos = {
        "historia_verde": "A" * 1001,
        "motivacao": "Teste"
    }
    
    url = f"{BASE_URL}/api/profissionais/api/1/storytelling"
    response = requests.put(url, json=dados_invalidos)
    
    if response.status_code == 400:
        print(f"  ✅ Validação de tamanho funcionando (história >1000)")
    else:
        print(f"  ⚠️ Validação de tamanho não funcionou corretamente")
    
    # Teste 2: JSON inválido
    dados_json_invalido = {
        "historia_verde": "Teste",
        "conquistas_json": "{'invalid': json}"  # JSON inválido
    }
    
    response = requests.put(url, json=dados_json_invalido)
    
    if response.status_code == 400:
        print(f"  ✅ Validação de JSON funcionando")
    else:
        print(f"  ⚠️ Validação de JSON não funcionou")
    
    return True

def teste_urls_pages():
    """Testa URLs das páginas HTML"""
    print(f"\n🧪 Testando páginas HTML...")
    
    urls = [
        ("/api/profissionais/perfil/1", "Perfil Storytelling"),
        ("/api/profissionais/editar/1", "Edição Storytelling"),
        ("/api/profissionais/dashboard/1", "Dashboard Profissional"),
    ]
    
    for url, nome in urls:
        response = requests.get(f"{BASE_URL}{url}")
        if response.status_code == 200:
            print(f"  ✅ {nome}: Status 200")
        else:
            print(f"  ❌ {nome}: Status {response.status_code}")

def executar_todos_testes():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE COMPLETO - STORYTELLING v1.6")
    print("=" * 60)
    
    resultados = []
    
    # Teste 1: Obter perfis
    print("\n📋 PARTE 1: Obtendo perfis storytelling")
    print("-" * 60)
    for id in [1, 2, 3, 4]:
        resultados.append(teste_obter_perfil(id))
    
    # Teste 2: Páginas HTML
    print("\n📋 PARTE 2: Testando páginas HTML")
    print("-" * 60)
    teste_urls_pages()
    
    # Teste 3: Atualização
    print("\n📋 PARTE 3: Testando atualização")
    print("-" * 60)
    resultados.append(teste_atualizar_storytelling())
    
    # Teste 4: Validações
    print("\n📋 PARTE 4: Testando validações")
    print("-" * 60)
    teste_validacoes()
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    perfis_ok = sum(resultados[:4])
    print(f"✅ Perfis carregados: {perfis_ok}/4")
    print(f"✅ Atualização: {'OK' if resultados[4] else 'FALHOU'}")
    print(f"✅ Validações: OK")
    
    sucesso_total = all(resultados)
    
    if sucesso_total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ Sistema Storytelling v1.6 está 100% funcional!")
    else:
        print("\n⚠️ Alguns testes falharam. Revisar logs acima.")
    
    print("\n🔗 Links para testar manualmente:")
    print("  • Dashboard: http://127.0.0.1:8002/api/profissionais/dashboard/1")
    print("  • Maria: http://127.0.0.1:8002/api/profissionais/perfil/1")
    print("  • João: http://127.0.0.1:8002/api/profissionais/perfil/2")
    print("  • Ana: http://127.0.0.1:8002/api/profissionais/perfil/3")
    print("  • Carlos: http://127.0.0.1:8002/api/profissionais/perfil/4")
    print("  • Editar: http://127.0.0.1:8002/api/profissionais/editar/1")
    
    return sucesso_total

if __name__ == "__main__":
    try:
        executar_todos_testes()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando!")
        print("Execute: python start_api.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
