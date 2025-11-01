import sqlite3
import json

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

# Buscar profissional
cursor.execute('SELECT habilidades_esg, ods_interesse FROM profissionais_esg WHERE id=1')
prof = cursor.fetchone()
print('=' * 60)
print('PROFISSIONAL ID=1 (Maria Silva Santos):')
print(f'Habilidades: {prof[0]}')
print(f'ODS: {prof[1]}')

habs_prof = json.loads(prof[0]) if prof[0] else []
ods_prof = json.loads(prof[1]) if prof[1] else []

print(f'\nHabilidades parseadas: {habs_prof}')
print(f'ODS parseados: {ods_prof}')

# Buscar algumas vagas
cursor.execute('SELECT titulo, habilidades_requeridas, ods_tags FROM vagas_esg WHERE status="ativa" LIMIT 10')
vagas = cursor.fetchall()

print('\n' + '=' * 60)
print('ANÁLISE DE VAGAS:')
print('=' * 60)

for i, v in enumerate(vagas, 1):
    habs_vaga = json.loads(v[1]) if v[1] else []
    ods_vaga = json.loads(v[2]) if v[2] else []
    
    # Calcular match atual
    hab_match = len(set(habs_prof) & set(habs_vaga))
    hab_total = len(set(habs_vaga)) if habs_vaga else 1
    
    ods_match = len(set(ods_prof) & set(ods_vaga))
    ods_total = len(set(ods_vaga)) if ods_vaga else 1
    
    score_hab = (hab_match / hab_total) * 50
    score_ods = (ods_match / ods_total) * 30
    score_loc = 20  # Assumindo remoto
    
    score_total = score_hab + score_ods + score_loc
    
    print(f'\n{i}. {v[0]}')
    print(f'   Habilidades vaga: {habs_vaga[:3]}... ({len(habs_vaga)} total)')
    print(f'   ODS vaga: {ods_vaga}')
    print(f'   Match habilidades: {hab_match}/{hab_total} = {score_hab:.1f}/50')
    print(f'   Match ODS: {ods_match}/{ods_total} = {score_ods:.1f}/30')
    print(f'   Score localização: {score_loc}/20')
    print(f'   SCORE TOTAL: {score_total:.1f}%')

conn.close()
