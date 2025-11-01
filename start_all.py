r"""
Launcher único para desenvolvimento do sistema Green Jobs Brasil.

Este script garante que o banco esteja inicializado e, em seguida,
inicia o servidor (uvicorn). Uso pensado para desenvolvimento local.

Como usar (PowerShell):
    py -3 .\start_all.py

Observação: este script delega para `start_api.start_api()` para manter
comportamento consistente com o `start_api.py` existente.
"""
import os
import sys
import time
from api.logger import logger


def main():
    # Garante que estamos no diretório do projeto
    repo_root = os.path.abspath(os.path.dirname(__file__))
    os.chdir(repo_root)
    # Importar o módulo principal da API para registrar routers e objetos
    try:
        # import side-effects (api.main normalmente inicializa app)
        import api.main  # noqa: F401
    except Exception as e:
        logger.exception("Erro ao importar 'api.main': %s", e)
        raise

    # Inicializa o banco explicitamente (idempotente)
    try:
        from api import db as api_db
        api_db.init_database()
    except Exception as e:
        logger.exception("Falha ao inicializar banco de dados: %s", e)
        raise

    # Informação amigável em Português
    logger.info("Inicialização concluída. Iniciando servidor de desenvolvimento...")
    logger.info("Acesse: http://127.0.0.1:8002/docs")

    # Reaproveitar o launcher existente (usa uvicorn em subprocess)
    try:
        import start_api
        start_api.start_api()
    except Exception as e:
        logger.exception("Erro ao tentar iniciar o servidor via start_api: %s", e)
        logger.info("Tentando iniciar uvicorn programaticamente...")

        # Fallback: iniciar uvicorn programaticamente (requer uvicorn instalado)
        try:
            import uvicorn

            # Executa uvicorn apontando para a aplicação FastAPI definida em api.main
            uvicorn.run("api.main:app", host="127.0.0.1", port=8002, reload=False)
        except Exception as e2:
            logger.exception("Falha ao iniciar uvicorn programaticamente: %s", e2)
            raise


if __name__ == "__main__":
    main()
