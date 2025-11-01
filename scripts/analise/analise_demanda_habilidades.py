import sqlite3
import json
from collections import Counter

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("=" * 70)
print("ANÁLISE DE HABILIDADES MAIS DEMANDADAS")
print("=" * 70)

# Buscar todas as habilidades das vagas
cursor.execute('SELECT habilidades_requeridas FROM vagas_esg WHERE status="ativa"')
vagas = cursor.fetchall()

todas_habilidades = []
for vaga in vagas:
    if vaga[0]:
        try:
            habs = json.loads(vaga[0])
            todas_habilidades.extend(habs)
        except:
            pass

# Contar frequência
counter = Counter(todas_habilidades)

print(f"\n📊 TOP 20 HABILIDADES MAIS DEMANDADAS:\n")
for i, (hab, count) in enumerate(counter.most_common(20), 1):
    print(f"{i:2}. {hab:40} - {count:2} vagas")

# Analisar ODS
print("\n" + "=" * 70)
print("ANÁLISE DE ODS MAIS DEMANDADOS")
print("=" * 70)

cursor.execute('SELECT ods_tags FROM vagas_esg WHERE status="ativa"')
vagas_ods = cursor.fetchall()

todos_ods = []
for vaga in vagas_ods:
    if vaga[0]:
        try:
            ods = json.loads(vaga[0])
            for o in ods:
                # Extrair número
                if isinstance(o, int):
                    todos_ods.append(o)
                elif isinstance(o, str):
                    import re
                    match = re.search(r'ODS\s*(\d+)', o, re.IGNORECASE)
                    if match:
                        todos_ods.append(int(match.group(1)))
        except:
            pass

counter_ods = Counter(todos_ods)

print(f"\n🌱 TOP 10 ODS MAIS DEMANDADOS:\n")
for i, (ods, count) in enumerate(counter_ods.most_common(10), 1):
    print(f"{i:2}. ODS {ods:2} - {count:2} vagas")

# Ver perfil atual da Maria
print("\n" + "=" * 70)
print("PERFIL ATUAL - MARIA SILVA SANTOS")
print("=" * 70)

cursor.execute('SELECT habilidades_esg, ods_interesse FROM profissionais_esg WHERE id=1')
maria = cursor.fetchone()

habs_maria = json.loads(maria[0]) if maria[0] else []
ods_maria = json.loads(maria[1]) if maria[1] else []

print(f"\n🎯 Habilidades atuais ({len(habs_maria)}):")
for hab in habs_maria:
    print(f"   • {hab}")

print(f"\n🌱 ODS atuais ({len(ods_maria)}):")
print(f"   {ods_maria}")

# Sugestões
print("\n" + "=" * 70)
print("💡 SUGESTÕES PARA MELHORAR PERFIL")
print("=" * 70)

# Habilidades que faltam
habs_sugeridas = []
for hab, count in counter.most_common(15):
    if hab not in habs_maria and count >= 3:  # Habilidades em 3+ vagas
        habs_sugeridas.append(hab)

print(f"\n✅ Adicionar estas habilidades (aparecem em muitas vagas):")
for i, hab in enumerate(habs_sugeridas[:10], 1):
    print(f"{i:2}. {hab}")

# ODS que faltam
ods_sugeridos = []
for ods, count in counter_ods.most_common(10):
    if ods not in ods_maria:
        ods_sugeridos.append(ods)

print(f"\n🌱 Adicionar estes ODS:")
print(f"   Atuais: {ods_maria}")
print(f"   Sugeridos: {ods_sugeridos[:5]}")

conn.close()

print("\n" + "=" * 70)
