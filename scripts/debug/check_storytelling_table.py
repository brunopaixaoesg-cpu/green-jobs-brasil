"""Verificar estrutura da tabela storytelling"""
import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
cursor = conn.cursor()

# Estrutura da tabela storytelling
cursor.execute('PRAGMA table_info(storytelling)')
cols = cursor.fetchall()

print("📖 Estrutura da tabela storytelling:\n")
for col in cols:
    nullable = "NULL" if not col[3] else "NOT NULL"
    default = f" DEFAULT {col[4]}" if col[4] else ""
    print(f"  {col[1]:30} {col[2]:15} {nullable}{default}")

print(f"\n📊 Total de colunas: {len(cols)}")

# Ver quantos registros tem
cursor.execute('SELECT COUNT(*) FROM storytelling')
count = cursor.fetchone()[0]
print(f"📝 Registros na tabela: {count}")

# Ver campos relacionados a imagem
print("\n📸 Campos de imagem:")
image_fields = [col for col in cols if any(keyword in col[1].lower() for keyword in ['foto', 'banner', 'url'])]
if image_fields:
    for col in image_fields:
        print(f"  ✓ {col[1]} ({col[2]})")
else:
    print("  ❌ Nenhum campo de imagem encontrado!")

conn.close()
