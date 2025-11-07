"""
Configuração de Logging Estruturado - Green Jobs Brasil
Suporta logs em texto (desenvolvimento) e JSON (produção)
"""
import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

from api.config import Config


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Formatter JSON customizado com campos adicionais"""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Adicionar campos customizados
        log_record['timestamp'] = self.formatTime(record, self.datefmt)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno
        
        # Informações do ambiente
        log_record['environment'] = 'production' if not Config.DEBUG else 'development'
        log_record['app_version'] = '1.6.0'


def setup_logging():
    """
    Configura o sistema de logging com base nas variáveis de ambiente
    
    - LOG_FORMAT: 'text' (desenvolvimento) ou 'json' (produção)
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL
    - LOG_DIR: Diretório para arquivos de log
    - LOG_FILE: Nome do arquivo de log
    - LOG_MAX_SIZE_MB: Tamanho máximo do arquivo antes de rotacionar
    - LOG_BACKUP_COUNT: Número de backups a manter
    """
    
    # Nome do logger principal
    logger_name = "green_jobs"
    logger = logging.getLogger(logger_name)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Configurar nível de log
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # ======================================
    # CONSOLE HANDLER
    # ======================================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if Config.LOG_FORMAT == "json":
        # Formato JSON para produção
        json_formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(logger)s %(module)s %(function)s %(line)s %(message)s'
        )
        console_handler.setFormatter(json_formatter)
    else:
        # Formato texto para desenvolvimento
        text_formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(text_formatter)
    
    logger.addHandler(console_handler)
    
    # ======================================
    # FILE HANDLER COM ROTATION
    # ======================================
    try:
        log_path = Config.get_log_path()
        
        # Garantir que o diretório existe
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Tamanho máximo em bytes
        max_bytes = Config.LOG_MAX_SIZE_MB * 1024 * 1024
        
        # Rotating file handler
        file_handler = RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max_bytes,
            backupCount=Config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        if Config.LOG_FORMAT == "json":
            file_handler.setFormatter(json_formatter)
        else:
            file_handler.setFormatter(text_formatter)
        
        logger.addHandler(file_handler)
        
        logger.info(f"Logging configurado: {log_path}")
        logger.info(f"Nível: {Config.LOG_LEVEL} | Formato: {Config.LOG_FORMAT}")
        logger.info(f"Rotation: {Config.LOG_MAX_SIZE_MB}MB | Backups: {Config.LOG_BACKUP_COUNT}")
        
    except Exception as e:
        logger.error(f"Erro ao configurar file handler: {e}")
        logger.warning("Continuando apenas com console logging")
    
    # ======================================
    # CONFIGURAÇÕES ADICIONAIS
    # ======================================
    
    # Desabilitar propagação para evitar logs duplicados
    logger.propagate = False
    
    # Configurar loggers de bibliotecas externas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logger


# ======================================
# INICIALIZAÇÃO AUTOMÁTICA
# ======================================
logger = setup_logging()


# ======================================
# FUNÇÕES DE UTILIDADE
# ======================================

def log_request(method: str, path: str, status_code: int, duration_ms: float):
    """
    Log estruturado de requisições HTTP
    
    Args:
        method: Método HTTP (GET, POST, etc)
        path: Caminho da requisição
        status_code: Código de status HTTP
        duration_ms: Duração em milissegundos
    """
    extra = {
        'http_method': method,
        'http_path': path,
        'http_status': status_code,
        'duration_ms': round(duration_ms, 2),
        'event_type': 'http_request'
    }
    
    if status_code >= 500:
        logger.error(f"{method} {path} {status_code} ({duration_ms:.2f}ms)", extra=extra)
    elif status_code >= 400:
        logger.warning(f"{method} {path} {status_code} ({duration_ms:.2f}ms)", extra=extra)
    else:
        logger.info(f"{method} {path} {status_code} ({duration_ms:.2f}ms)", extra=extra)


def log_db_query(query: str, duration_ms: float, rows_affected: int = 0):
    """
    Log estruturado de queries de banco de dados
    
    Args:
        query: Query SQL (truncada se muito longa)
        duration_ms: Duração em milissegundos
        rows_affected: Número de linhas afetadas
    """
    # Truncar query se muito longa
    query_preview = query[:100] + "..." if len(query) > 100 else query
    
    extra = {
        'db_query': query_preview,
        'duration_ms': round(duration_ms, 2),
        'rows_affected': rows_affected,
        'event_type': 'db_query'
    }
    
    if duration_ms > 1000:  # Mais de 1 segundo
        logger.warning(f"SLOW QUERY ({duration_ms:.2f}ms): {query_preview}", extra=extra)
    else:
        logger.debug(f"Query ({duration_ms:.2f}ms): {query_preview}", extra=extra)


def log_error(error: Exception, context: dict = None):
    """
    Log estruturado de erros com contexto adicional
    
    Args:
        error: Exceção capturada
        context: Dicionário com contexto adicional
    """
    extra = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'event_type': 'error'
    }
    
    if context:
        extra.update(context)
    
    logger.error(f"Erro: {type(error).__name__}: {error}", extra=extra, exc_info=True)


def log_metric(metric_name: str, value: float, unit: str = None, tags: dict = None):
    """
    Log estruturado de métricas (útil para integração com Prometheus)
    
    Args:
        metric_name: Nome da métrica
        value: Valor da métrica
        unit: Unidade (ms, bytes, count, etc)
        tags: Tags adicionais
    """
    extra = {
        'metric_name': metric_name,
        'metric_value': value,
        'metric_unit': unit or 'count',
        'event_type': 'metric'
    }
    
    if tags:
        extra.update(tags)
    
    logger.info(f"Metric: {metric_name}={value}{unit or ''}", extra=extra)


# ======================================
# EXPORTS
# ======================================
__all__ = [
    'logger',
    'log_request',
    'log_db_query',
    'log_error',
    'log_metric'
]
