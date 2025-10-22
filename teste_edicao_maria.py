"""
Teste de edição manual do perfil de Maria
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

print("🧪 Testando edição do perfil de Maria (ID 1)\n")

# Dados de teste
dados_maria_atualizada = {
    "historia_verde": "Minha jornada ESG começou há 5 anos quando percebi o impacto real das mudanças climáticas. Desde então, trabalho para transformar empresas em agentes de mudança positiva, implementando práticas sustentáveis que geram resultados mensuráveis. Já ajudei mais de 15 empresas a reduzirem suas emissões e melhorarem seus indicadores ESG.",
    "motivacao": "Acredito que cada ação conta e que empresas têm o poder de liderar a transição para uma economia verde. Meu objetivo é provar que sustentabilidade e lucratividade caminham juntas.",
    "valores_pessoais": "Transparência, Impacto Real, Colaboração, Inovação Sustentável, Responsabilidade",
    "objetivos_carreira": "Liderar programas de transformação ESG em grandes corporações e desenvolver uma consultoria própria focada em pequenas e médias empresas.",
    "conquistas_json": json.dumps([
        {
            "titulo": "Redução de 40% nas Emissões",
            "descricao": "Implementei programa que reduziu emissões de CO2 em 40% em grande indústria",
            "data": "2024",
            "icone": "🌍"
        },
        {
            "titulo": "Certificação ISO 14001",
            "descricao": "Lideração no processo de certificação ambiental internacional",
            "data": "2023",
            "icone": "🏆"
        },
        {
            "titulo": "Prêmio ESG Excellence",
            "descricao": "Reconhecimento por projeto inovador de economia circular",
            "data": "2023",
            "icone": "⭐"
        },
        {
            "titulo": "15+ Empresas Transformadas",
            "descricao": "Total de organizações que implementaram programas ESG sob minha coordenação",
            "data": "2019-2024",
            "icone": "📊"
        }
    ], ensure_ascii=False),
    "portfolio_projetos_json": json.dumps([
        {
            "titulo": "Sistema de Reciclagem Industrial",
            "empresa": "TechManufacturing S.A.",
            "descricao": "Implementação completa de sistema de reciclagem que transformou 90% dos resíduos industriais em matéria-prima reutilizável.",
            "periodo": "Jan 2023 - Dez 2023",
            "resultados": ["90% de materiais reciclados", "R$500mil em economia anual", "300 toneladas CO2 evitadas"],
            "ods": [12, 13, 9],
            "tecnologias": ["Análise de Ciclo de Vida", "Gestão de Resíduos", "Power BI"]
        },
        {
            "titulo": "Transição para Energia Renovável",
            "empresa": "EcoLogistics LTDA",
            "descricao": "Projeto de migração completa da matriz energética para fontes 100% renováveis, incluindo instalação de painéis solares e contratos de energia verde.",
            "periodo": "Jun 2022 - Mai 2023",
            "resultados": ["100% energia renovável", "60% redução custos energia", "Payback em 5 anos"],
            "ods": [7, 13],
            "tecnologias": ["Energia Solar", "Análise de Viabilidade", "Excel Avançado"]
        },
        {
            "titulo": "Inventário de Emissões GEE",
            "empresa": "Rede Varejo Verde",
            "descricao": "Estruturação e execução do primeiro inventário completo de gases de efeito estufa em rede com 50 lojas, estabelecendo linha de base para metas de neutralidade.",
            "periodo": "Mar 2021 - Out 2021",
            "resultados": ["1.200 tonCO2eq mapeadas", "Plano de redução 5 anos", "Selo Carbono Neutro"],
            "ods": [13, 17],
            "tecnologias": ["GHG Protocol", "Metodologia IPCC", "Relatório GRI"]
        }
    ], ensure_ascii=False),
    "idiomas_json": json.dumps([
        {"idioma": "Português", "nivel": "Nativo"},
        {"idioma": "Inglês", "nivel": "Fluente"},
        {"idioma": "Espanhol", "nivel": "Intermediário"}
    ], ensure_ascii=False)
}

print("📝 Dados a serem salvos:")
print(f"  História: {len(dados_maria_atualizada['historia_verde'])} caracteres")
print(f"  Conquistas: 4 items")
print(f"  Projetos: 3 items")
print(f"  Idiomas: 3 items\n")

# Fazer PUT
url = f"{BASE_URL}/api/profissionais/api/1/storytelling"
response = requests.put(url, json=dados_maria_atualizada)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Salvamento bem-sucedido!")
    print(f"   Resposta: {result}\n")
    
    # Verificar se foi salvo
    print("🔍 Verificando se dados foram persistidos...")
    response_get = requests.get(url)
    if response_get.status_code == 200:
        data = response_get.json()
        print(f"✅ História carregada: {len(data.get('historia_verde', ''))} chars")
        print(f"✅ Conquistas: {len(data.get('conquistas', []))} items")
        print(f"✅ Projetos: {len(data.get('portfolio_projetos', []))} items")
        print(f"✅ Idiomas: {len(data.get('idiomas', []))} items")
        
        if "transformar empresas em agentes de mudança" in data.get('historia_verde', ''):
            print(f"\n🎉 SUCESSO! Dados foram salvos e carregados corretamente!")
            print(f"\n🔗 Veja o perfil: http://127.0.0.1:8002/api/profissionais/perfil/1")
        else:
            print(f"\n⚠️ Dados parecem diferentes do esperado")
    else:
        print(f"❌ Erro ao carregar: {response_get.status_code}")
else:
    print(f"❌ Erro ao salvar: {response.status_code}")
    print(f"   {response.text}")
