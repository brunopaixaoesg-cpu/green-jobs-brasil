"""Verificar campos de imagem na tabela profissionais_esg"""
import sqlite3

conn = sqlite3.connect('api/gjb_dev.db')
cursor = conn.cursor()

# Listar todas as colunas
cursor.execute('PRAGMA table_info(profissionais_esg)')
cols = cursor.fetchall()

print("📸 Verificando campos de imagem no banco\n")
print("Campos relacionados a foto/banner/url:")
image_fields = [col for col in cols if any(keyword in col[1].lower() for keyword in ['foto', 'banner', 'url'])]

if image_fields:
    for col in image_fields:
        print(f"  ✓ {col[1]} ({col[2]})")
else:
    print("  ❌ Nenhum campo de imagem encontrado!")

print(f"\n📊 Total de colunas: {len(cols)}")

# Mostrar estrutura completa se necessário
print("\n📋 Estrutura completa da tabela:")
for col in cols:
    print(f"  - {col[1]} ({col[2]})")

conn.close()
