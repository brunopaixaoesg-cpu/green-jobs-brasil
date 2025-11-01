import sys
import os
sys.path.append('api')

from sqlite_api_clean import init_database, get_db
from scripts.db_wrapper import get_connection

print("🧪 Testando inicialização do banco...")

# Deletar banco se existir
if os.path.exists('api/gjb_dev.db'):
    os.remove('api/gjb_dev.db')
    print("🗑️ Banco antigo removido")

# Executar init_database
try:
    init_database()
    print("✅ Função init_database executada")
except Exception as e:
    print(f"❌ Erro na init_database: {e}")

# Verificar resultado
if os.path.exists('api/gjb_dev.db'):
    print(f"📏 Tamanho do banco: {os.path.getsize('api/gjb_dev.db')} bytes")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tabelas criadas: {[t[0] for t in tables]}")
else:
    print("❌ Banco não foi criado")