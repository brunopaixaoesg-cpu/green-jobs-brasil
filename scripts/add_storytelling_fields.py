"""
Script para adicionar campos de storytelling ao perfil profissional
Versão v1.6 - Storytelling Profissional
"""
import sqlite3
from datetime import datetime

print("="*70)
print("🎨 ADICIONANDO CAMPOS DE STORYTELLING - v1.6")
print("="*70)

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Lista de novos campos
novos_campos = [
    ("historia_verde", "TEXT", "Narrativa pessoal da jornada ESG"),
    ("motivacao", "TEXT", "O que motiva o profissional"),
    ("conquistas_json", "TEXT", "JSON com conquistas e marcos"),
    ("portfolio_projetos_json", "TEXT", "JSON com projetos ESG realizados"),
    ("valores_pessoais", "TEXT", "Valores que guiam a carreira"),
    ("objetivos_carreira", "TEXT", "Objetivos profissionais futuros"),
    ("foto_perfil_url", "TEXT", "URL da foto de perfil"),
    ("banner_url", "TEXT", "URL do banner do perfil"),
    ("redes_sociais_json", "TEXT", "JSON com links de redes sociais"),
    ("idiomas_json", "TEXT", "JSON com idiomas e níveis"),
    ("voluntariado_json", "TEXT", "JSON com trabalhos voluntários"),
    ("publicacoes_json", "TEXT", "JSON com artigos/publicações")
]

print("\n📊 Verificando estrutura atual da tabela profissionais_esg...")
cursor.execute("PRAGMA table_info(profissionais_esg)")
colunas_existentes = {col[1] for col in cursor.fetchall()}
print(f"   Total de colunas existentes: {len(colunas_existentes)}")

print("\n✨ Adicionando novos campos:")
print("-"*70)

campos_adicionados = 0
campos_existentes = 0

for campo, tipo, descricao in novos_campos:
    if campo in colunas_existentes:
        print(f"   ⚠️  {campo:30} - Já existe")
        campos_existentes += 1
    else:
        try:
            cursor.execute(f"ALTER TABLE profissionais_esg ADD COLUMN {campo} {tipo}")
            print(f"   ✅ {campo:30} - Adicionado ({descricao})")
            campos_adicionados += 1
        except Exception as e:
            print(f"   ❌ {campo:30} - Erro: {e}")

conn.commit()

print("\n" + "="*70)
print(f"📈 RESUMO:")
print(f"   ✅ Campos adicionados: {campos_adicionados}")
print(f"   ⚠️  Campos já existentes: {campos_existentes}")
print("="*70)

# Criar dados exemplo para Maria (profissional_id=1)
print("\n🎨 Criando dados exemplo para Maria Silva Santos...")

historia_verde = """
Minha jornada na sustentabilidade começou há 5 anos, quando percebi o impacto 
que as empresas podem ter no meio ambiente. Desde então, dedico-me a ajudar 
organizações a reduzirem sua pegada de carbono e implementarem práticas ESG 
realmente transformadoras.

Já ajudei mais de 15 empresas a conquistarem certificações ambientais e reduzirem 
emissões em até 40%. Cada projeto é uma oportunidade de fazer a diferença real 
no planeta que deixaremos para as próximas gerações.
"""

motivacao = """
Acredito que negócios sustentáveis são o futuro. Minha motivação vem de ver 
empresas transformando lucro e propósito em uma só missão, provando que é 
possível crescer economicamente enquanto se protege o meio ambiente.
"""

import json

conquistas = json.dumps([
    {
        "titulo": "40% de Redução de Emissões",
        "descricao": "Liderou projeto que reduziu emissões de CO2 em 40% em indústria",
        "data": "2024-03",
        "icon": "🏆"
    },
    {
        "titulo": "Certificação ISO 14001",
        "descricao": "Implementou sistema de gestão ambiental em 3 empresas",
        "data": "2023-11",
        "icon": "✅"
    },
    {
        "titulo": "Prêmio Inovação Verde",
        "descricao": "Reconhecida como Profissional ESG do Ano 2023",
        "data": "2023-12",
        "icon": "🌟"
    },
    {
        "titulo": "15+ Empresas Transformadas",
        "descricao": "Consultoria ESG implementada com sucesso",
        "data": "2024-10",
        "icon": "🌱"
    }
])

portfolio_projetos = json.dumps([
    {
        "titulo": "Sistema de Reciclagem Industrial",
        "empresa": "Indústria XYZ Ltda",
        "periodo": "Jan 2024 - Jun 2024",
        "descricao": "Implementação de sistema completo de reciclagem e reuso de resíduos industriais",
        "resultados": [
            "90% dos resíduos agora são reciclados",
            "R$ 500k economizados anualmente",
            "300 toneladas de CO2 evitadas por ano"
        ],
        "ods": [12, 13, 9],
        "tecnologias": ["IoT", "Sensores", "Análise de Dados"],
        "imagem_url": None
    },
    {
        "titulo": "Transição para Energia Renovável",
        "empresa": "Fábrica ABC SA",
        "periodo": "Mar 2023 - Dez 2023",
        "descricao": "Projeto de migração completa para energia solar e eólica",
        "resultados": [
            "100% energia renovável",
            "60% redução de custos energéticos",
            "Payback em 4 anos"
        ],
        "ods": [7, 13],
        "tecnologias": ["Painéis Solares", "Turbinas Eólicas", "Smart Grid"],
        "imagem_url": None
    },
    {
        "titulo": "Inventário GEE e Compensação",
        "empresa": "Tech Verde Corp",
        "periodo": "Set 2023 - Nov 2023",
        "descricao": "Primeiro inventário de gases de efeito estufa e plano de compensação",
        "resultados": [
            "1.200 toneladas CO2e mapeadas",
            "Plano de redução de 5 anos",
            "Selo Carbono Neutro conquistado"
        ],
        "ods": [13, 17],
        "tecnologias": ["GHG Protocol", "Software de Inventário", "Blockchain"],
        "imagem_url": None
    }
])

valores_pessoais = "Transparência, Impacto Real, Colaboração, Inovação Sustentável, Responsabilidade"

objetivos_carreira = """
Nos próximos 3 anos, quero liderar a transformação ESG de grandes corporações, 
ajudando-as a atingir Net Zero. Também planejo lançar uma consultoria própria 
focada em startups verdes e escrever um livro sobre ESG prático para pequenas 
e médias empresas.
"""

redes_sociais = json.dumps({
    "linkedin": "linkedin.com/in/maria-silva-santos-esg",
    "twitter": "@mariaesg",
    "github": None,
    "medium": "medium.com/@mariaesg"
})

idiomas = json.dumps([
    {"idioma": "Português", "nivel": "Nativo"},
    {"idioma": "Inglês", "nivel": "Fluente"},
    {"idioma": "Espanhol", "nivel": "Intermediário"}
])

voluntariado = json.dumps([
    {
        "organizacao": "ONG Plantando o Futuro",
        "papel": "Consultora Voluntária",
        "periodo": "2023 - Presente",
        "descricao": "Auxílio em projetos de reflorestamento e educação ambiental"
    },
    {
        "organizacao": "Instituto Clima Agora",
        "papel": "Mentora",
        "periodo": "2022 - 2023",
        "descricao": "Mentoria de jovens profissionais entrando na área ESG"
    }
])

publicacoes = json.dumps([
    {
        "titulo": "ESG na Prática: 10 Passos para Pequenas Empresas",
        "tipo": "Artigo",
        "veiculo": "Medium",
        "data": "2024-05",
        "url": "medium.com/@mariaesg/esg-na-pratica"
    },
    {
        "titulo": "Inventário GEE: Guia Completo",
        "tipo": "E-book",
        "veiculo": "Próprio",
        "data": "2023-09",
        "url": None
    }
])

try:
    cursor.execute("""
        UPDATE profissionais_esg 
        SET historia_verde = ?,
            motivacao = ?,
            conquistas_json = ?,
            portfolio_projetos_json = ?,
            valores_pessoais = ?,
            objetivos_carreira = ?,
            redes_sociais_json = ?,
            idiomas_json = ?,
            voluntariado_json = ?,
            publicacoes_json = ?
        WHERE id = 1
    """, (
        historia_verde.strip(),
        motivacao.strip(),
        conquistas,
        portfolio_projetos,
        valores_pessoais,
        objetivos_carreira.strip(),
        redes_sociais,
        idiomas,
        voluntariado,
        publicacoes
    ))
    
    conn.commit()
    print("   ✅ Dados de Maria atualizados com sucesso!")
    
    # Verificar
    cursor.execute("""
        SELECT nome_completo, 
               LENGTH(historia_verde) as hist_len,
               LENGTH(portfolio_projetos_json) as port_len,
               conquistas_json
        FROM profissionais_esg 
        WHERE id = 1
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"\n   📊 Perfil de {result[0]}:")
        print(f"      - História: {result[1]} caracteres")
        print(f"      - Portfólio: {result[2]} caracteres")
        
        conquistas_data = json.loads(result[3])
        print(f"      - Conquistas: {len(conquistas_data)} itens")
        
except Exception as e:
    print(f"   ❌ Erro ao atualizar dados: {e}")
    conn.rollback()

conn.close()

print("\n" + "="*70)
print("✅ BANCO ATUALIZADO COM SUCESSO!")
print("="*70)
print("\n💡 Próximo passo: Criar componentes visuais no dashboard")
print()
