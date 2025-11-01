"""
Script para iniciar a API do Green Jobs Brasil
"""
import subprocess
import sys
import os
from api.logger import logger

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
    
    logger.info("Iniciando Green Jobs Brasil API...")
    logger.info("API: http://127.0.0.1:8002")
    logger.info("Docs: http://127.0.0.1:8002/docs")
    logger.info("%s", "=" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        logger.info("API interrompida pelo usuario")
    except Exception as e:
        logger.exception("Erro ao iniciar API: %s", e)

if __name__ == "__main__":
    start_api()