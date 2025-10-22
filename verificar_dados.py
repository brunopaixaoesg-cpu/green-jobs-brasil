import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("\n📊 Verificando dados de storytelling no banco:\n")

cursor.execute("""
    SELECT id, nome_completo, 
           LENGTH(historia_verde) as hist_len,
           LENGTH(conquistas_json) as conq_len,
           LENGTH(portfolio_projetos_json) as proj_len
    FROM profissionais_esg 
    WHERE id IN (1,2,3,4)
    ORDER BY id
""")

for row in cursor.fetchall():
    id, nome, hist, conq, proj = row
    print(f"ID {id}: {nome}")
    print(f"  História: {hist if hist else 0} chars")
    print(f"  Conquistas JSON: {conq if conq else 0} chars")
    print(f"  Projetos JSON: {proj if proj else 0} chars")
    print()

conn.close()
