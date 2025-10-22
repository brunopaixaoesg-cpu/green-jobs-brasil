import sqlite3
import json

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("=" * 70)
print("ENRIQUECENDO PERFIL - MARIA SILVA SANTOS")
print("=" * 70)

# Perfil atual
cursor.execute('SELECT habilidades_esg, ods_interesse FROM profissionais_esg WHERE id=1')
maria = cursor.fetchone()
habs_atual = json.loads(maria[0]) if maria[0] else []
ods_atual = json.loads(maria[1]) if maria[1] else []

print(f"\n📋 ANTES:")
print(f"   Habilidades ({len(habs_atual)}): {habs_atual}")
print(f"   ODS ({len(ods_atual)}): {ods_atual}")

# Novas habilidades (mantendo as atuais + adicionando as mais demandadas)
novas_habilidades = [
    # Habilidades atuais (atualizadas)
    "Gestão Ambiental",
    "Relatórios ESG",
    "GRI Standards",
    "GRI",  # Adicionar versão curta também
    
    # Top habilidades demandadas
    "ISO 14001",
    "Inventário GEE",
    "Pegada de Carbono",
    "LCA",  # Life Cycle Assessment
    "Stakeholder Engagement",
    "Risk Assessment ESG",
    "Net Zero",
    "Energia Renovável",
    "Economia Circular",
    "Due Diligence ESG",
    "SASB",
    "Análise de Materialidade",
    "Mudanças Climáticas",
    "CDP",  # Carbon Disclosure Project
    "Biodiversidade",
    "TCFD",  # Task Force on Climate-related Financial Disclosures
]

# Novos ODS (mantendo os atuais + adicionando os mais demandados)
novos_ods = [7, 8, 9, 12, 13, 14, 15]  # 7 ODS principais

# Atualizar no banco
cursor.execute('''
    UPDATE profissionais_esg 
    SET habilidades_esg = ?,
        ods_interesse = ?,
        atualizado_em = CURRENT_TIMESTAMP
    WHERE id = 1
''', (json.dumps(novas_habilidades, ensure_ascii=False), 
      json.dumps(novos_ods)))

conn.commit()

print(f"\n✅ DEPOIS:")
print(f"   Habilidades ({len(novas_habilidades)}): {novas_habilidades[:5]}... (+{len(novas_habilidades)-5} mais)")
print(f"   ODS ({len(novos_ods)}): {novos_ods}")

# Verificar mudanças
cursor.execute('SELECT habilidades_esg, ods_interesse FROM profissionais_esg WHERE id=1')
maria_nova = cursor.fetchone()
habs_nova = json.loads(maria_nova[0])
ods_nova = json.loads(maria_nova[1])

print(f"\n📊 ESTATÍSTICAS:")
print(f"   Habilidades adicionadas: {len(habs_nova) - len(habs_atual)}")
print(f"   ODS adicionados: {len(ods_nova) - len(ods_atual)}")
print(f"   Total de habilidades: {len(habs_nova)}")
print(f"   Total de ODS: {len(ods_nova)}")

conn.close()

print("\n" + "=" * 70)
print("✅ PERFIL ENRIQUECIDO COM SUCESSO!")
print("=" * 70)
