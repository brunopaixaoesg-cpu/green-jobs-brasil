"""
Script para iniciar a API do Green Jobs Brasil
"""
import subprocess
import sys
import os

def start_api():
    # Mudar para o diretório do projeto
    os.chdir(r"C:\Users\Bruno\Empresas Verdes")
    
    # Comando para iniciar a API com uvicorn (PORTA PADRÃO: 8002)
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "api.main:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", "8002"
    ]
    
    print("🚀 Iniciando Green Jobs Brasil API...")
    print("📍 API: http://127.0.0.1:8002")
    print("📚 Docs: http://127.0.0.1:8002/docs")
    print("🔍 TSB: http://127.0.0.1:8002/api/taxonomia/objetivos")
    print("=" * 60)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⚠️  API interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_api()