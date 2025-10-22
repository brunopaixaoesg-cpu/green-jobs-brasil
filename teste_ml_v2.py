import requests
import json

# Login
login_data = {
    "username": "bruno@greenjobsbrasil.com.br",
    "password": "Senha123!"
}

print("=" * 70)
print("TESTANDO ALGORITMO ML v2 - SCORES REALISTAS")
print("=" * 70)

response = requests.post("http://127.0.0.1:8002/api/auth/login", data=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print("✅ Login OK\n")
    
    # Testar recomendações
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "http://127.0.0.1:8002/api/profissionais/me/recomendacoes?limit=10",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"📊 ALGORITMO: {data['algoritmo']}")
        print(f"📈 Total disponíveis: {data['total_disponiveis']}")
        print(f"✅ Total qualificadas (>30%): {data['total_qualificadas']}")
        print(f"\n🎯 CRITÉRIOS v2:")
        for k, v in data['criterios'].items():
            print(f"   • {k}: {v}")
        
        print(f"\n🆕 MELHORIAS:")
        melhorias = data.get('melhorias_v3') or data.get('melhorias_v2', [])
        for m in melhorias:
            print(f"   ✓ {m}")
        
        print("\n" + "=" * 70)
        print(f"TOP {len(data['vagas_recomendadas'])} RECOMENDAÇÕES:")
        print("=" * 70)
        
        for i, vaga in enumerate(data['vagas_recomendadas'], 1):
            score = vaga['compatibilidade_score']
            
            # Colorir score
            if score >= 70:
                nivel = "🟢 EXCELENTE"
            elif score >= 50:
                nivel = "🟡 BOM"
            elif score >= 30:
                nivel = "🟠 REGULAR"
            else:
                nivel = "🔴 FRACO"
            
            print(f"\n{i}. {vaga['titulo']}")
            print(f"   Score: {score}% {nivel}")
            print(f"   Nível: {vaga.get('nivel_experiencia', 'N/A')}")
            print(f"   Localização: {vaga.get('localizacao_cidade', 'N/A')}, {vaga.get('localizacao_uf', 'N/A')}")
            print(f"   Remoto: {'Sim' if vaga.get('remoto') else 'Não'}")
            
            if 'match_detalhes' in vaga:
                print(f"   Detalhes:")
                for k, v in vaga['match_detalhes'].items():
                    print(f"      • {k}: {v}")
        
        print("\n" + "=" * 70)
        print("✅ TESTE CONCLUÍDO!")
        print("=" * 70)
        
    else:
        print(f"❌ Erro nas recomendações: {response.status_code}")
        print(response.text)
else:
    print(f"❌ Erro no login: {response.status_code}")
