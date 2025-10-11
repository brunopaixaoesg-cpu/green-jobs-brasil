import sqlite3

conn = sqlite3.connect('gjb_dev.db')
cursor = conn.cursor()

print("CNAEs verdes relacionados a engenharia:")
cursor.execute("SELECT cnae, titulo FROM cnae_green WHERE cnae LIKE '%71.12%'")
results = cursor.fetchall()
for cnae, titulo in results:
    print(f"{cnae}: {titulo}")

print("\nTodos os CNAEs verdes:")
cursor.execute("SELECT cnae, titulo FROM cnae_green ORDER BY cnae")
all_results = cursor.fetchall()
for cnae, titulo in all_results:
    print(f"{cnae}: {titulo}")

conn.close()