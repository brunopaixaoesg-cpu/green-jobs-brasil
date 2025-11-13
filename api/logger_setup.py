"""
Sistema de logging estruturado para Green Jobs Brasil.
Suporta formato texto (desenvolvimento) e JSON (produção).
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from api.settings import settings


def setup_logging():
    """Configura sistema de logging da aplicação"""
    
    # Criar diretório de logs se não existir
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar nível de log
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Criar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remover handlers existentes
    root_logger.handlers.clear()
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Handler para arquivo com rotação
    file_handler = RotatingFileHandler(
        filename=log_dir / settings.log_file,
        maxBytes=settings.log_max_size_mb * 1024 * 1024,  # MB para bytes
        backupCount=settings.log_backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    
    # Definir formatters
    if settings.log_format == "json":
        # Formato JSON para produção
        json_formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(json_formatter)
        file_handler.setFormatter(json_formatter)
    else:
        # Formato texto para desenvolvimento
        text_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(text_formatter)
        file_handler.setFormatter(text_formatter)
    
    # Adicionar handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Silenciar logs verbose de bibliotecas
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Log de inicialização
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configurado - Level: {settings.log_level}, "
        f"Format: {settings.log_format}, "
        f"Environment: {settings.environment}"
    )


def get_logger(name: str) -> logging.Logger:
    """Retorna logger configurado para um módulo específico"""
    return logging.getLogger(name)


# Configurar logging ao importar
setup_logging()
