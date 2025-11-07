"""
Health Check Endpoints - P3.4
Rotas para monitoramento, health checks e métricas
"""
from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional
import time
import os
import psutil

from api.db import get_db, test_connection
from api.logging_config import logger
from api.config import Config

router = APIRouter(tags=["health"])

# ===== Response Models =====

class HealthResponse(BaseModel):
    """Response model para /health endpoint"""
    status: str
    timestamp: datetime
    version: str
    database: Dict[str, Any]
    uptime_seconds: Optional[float] = None

class ReadinessResponse(BaseModel):
    """Response model para /ready endpoint"""
    ready: bool
    timestamp: datetime
    checks: Dict[str, bool]
    message: str

class MetricsResponse(BaseModel):
    """Response model para /metrics endpoint"""
    timestamp: datetime
    system: Dict[str, Any]
    database: Dict[str, Any]
    api: Dict[str, Any]

# ===== Global State =====
_start_time = time.time()

# ===== Endpoints =====

@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """
    Health check endpoint - Verifica saúde geral da API
    
    Realiza:
    - Teste de conexão com banco de dados
    - Verificação de query simples (SELECT 1)
    - Tempo de resposta do DB
    
    Returns:
        HealthResponse: Status da API e conexões
    """
    db_status = {
        "connected": False,
        "response_time_ms": None,
        "error": None
    }
    
    try:
        start = time.time()
        conn = get_db()
        cursor = conn.cursor()
        
        # Simple health check query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        conn.close()
        
        db_status["connected"] = result is not None
        db_status["response_time_ms"] = round((time.time() - start) * 1000, 2)
        
    except Exception as e:
        logger.error(f"Health check DB error: {e}")
        db_status["error"] = str(e)
    
    overall_status = "healthy" if db_status["connected"] else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(),
        version=Config.APP_VERSION,
        database=db_status,
        uptime_seconds=round(time.time() - _start_time, 2)
    )

@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check(request: Request):
    """
    Readiness check endpoint - Para Kubernetes readiness probe
    
    Verifica se a API está pronta para receber tráfego:
    - Banco de dados acessível
    - Diretório de logs gravável
    - Arquivo de configuração carregado
    
    Returns:
        ReadinessResponse: Status de prontidão da API
    """
    checks = {
        "database": False,
        "logs_writable": False,
        "config_loaded": False
    }
    
    # Check 1: Database
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM empresas_esg")
        count = cursor.fetchone()[0]
        conn.close()
        checks["database"] = count >= 0
    except Exception as e:
        logger.error(f"Readiness check DB error: {e}")
    
    # Check 2: Logs writable
    try:
        log_dir = os.path.dirname(Config.get_log_path())
        checks["logs_writable"] = os.path.exists(log_dir) and os.access(log_dir, os.W_OK)
    except Exception as e:
        logger.error(f"Readiness check logs error: {e}")
    
    # Check 3: Config loaded
    try:
        checks["config_loaded"] = Config.APP_VERSION is not None
    except Exception as e:
        logger.error(f"Readiness check config error: {e}")
    
    # All checks must pass
    ready = all(checks.values())
    
    message = "Service is ready" if ready else "Service is not ready"
    
    return ReadinessResponse(
        ready=ready,
        timestamp=datetime.now(),
        checks=checks,
        message=message
    )

@router.get("/metrics")
async def metrics_endpoint(request: Request):
    """
    Metrics endpoint - Prometheus-compatible metrics
    
    Retorna métricas em formato Prometheus:
    - Uso de memória e CPU
    - Estatísticas de banco de dados
    - Uptime da aplicação
    
    Returns:
        str: Métricas em formato Prometheus (text/plain)
    """
    metrics = []
    
    # Uptime
    uptime = time.time() - _start_time
    metrics.append(f"# HELP greenjobs_uptime_seconds Application uptime in seconds")
    metrics.append(f"# TYPE greenjobs_uptime_seconds gauge")
    metrics.append(f"greenjobs_uptime_seconds {uptime:.2f}")
    
    # System metrics
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        
        metrics.append(f"# HELP greenjobs_memory_bytes Memory usage in bytes")
        metrics.append(f"# TYPE greenjobs_memory_bytes gauge")
        metrics.append(f"greenjobs_memory_bytes {memory_info.rss}")
        
        cpu_percent = process.cpu_percent()
        metrics.append(f"# HELP greenjobs_cpu_percent CPU usage percentage")
        metrics.append(f"# TYPE greenjobs_cpu_percent gauge")
        metrics.append(f"greenjobs_cpu_percent {cpu_percent}")
        
    except Exception as e:
        logger.error(f"Metrics system error: {e}")
    
    # Database metrics
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Count tables
        cursor.execute("SELECT COUNT(*) FROM empresas_esg")
        empresas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        profissionais_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vagas WHERE status='ativa'")
        vagas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM candidaturas")
        candidaturas_count = cursor.fetchone()[0]
        
        conn.close()
        
        metrics.append(f"# HELP greenjobs_empresas_total Total de empresas cadastradas")
        metrics.append(f"# TYPE greenjobs_empresas_total gauge")
        metrics.append(f"greenjobs_empresas_total {empresas_count}")
        
        metrics.append(f"# HELP greenjobs_profissionais_total Total de profissionais cadastrados")
        metrics.append(f"# TYPE greenjobs_profissionais_total gauge")
        metrics.append(f"greenjobs_profissionais_total {profissionais_count}")
        
        metrics.append(f"# HELP greenjobs_vagas_ativas Total de vagas ativas")
        metrics.append(f"# TYPE greenjobs_vagas_ativas gauge")
        metrics.append(f"greenjobs_vagas_ativas {vagas_count}")
        
        metrics.append(f"# HELP greenjobs_candidaturas_total Total de candidaturas")
        metrics.append(f"# TYPE greenjobs_candidaturas_total gauge")
        metrics.append(f"greenjobs_candidaturas_total {candidaturas_count}")
        
    except Exception as e:
        logger.error(f"Metrics database error: {e}")
    
    # Database health
    try:
        start = time.time()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        
        db_response_time = (time.time() - start) * 1000
        
        metrics.append(f"# HELP greenjobs_db_response_time_ms Database response time in milliseconds")
        metrics.append(f"# TYPE greenjobs_db_response_time_ms gauge")
        metrics.append(f"greenjobs_db_response_time_ms {db_response_time:.2f}")
        
        metrics.append(f"# HELP greenjobs_db_health Database health status (1=healthy, 0=unhealthy)")
        metrics.append(f"# TYPE greenjobs_db_health gauge")
        metrics.append(f"greenjobs_db_health 1")
        
    except Exception as e:
        logger.error(f"Metrics DB health error: {e}")
        metrics.append(f"# HELP greenjobs_db_health Database health status (1=healthy, 0=unhealthy)")
        metrics.append(f"# TYPE greenjobs_db_health gauge")
        metrics.append(f"greenjobs_db_health 0")
    
    # Return as plain text (Prometheus format)
    from fastapi.responses import Response
    return Response(
        content="\n".join(metrics) + "\n",
        media_type="text/plain; version=0.0.4"
    )

@router.get("/metrics/json", response_model=MetricsResponse)
async def metrics_json(request: Request):
    """
    Metrics endpoint in JSON format
    
    Mesmas métricas do /metrics mas em formato JSON
    para facilitar integração com outras ferramentas
    
    Returns:
        MetricsResponse: Métricas em formato JSON
    """
    system = {}
    database = {}
    api = {}
    
    # System metrics
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        
        system = {
            "memory_bytes": memory_info.rss,
            "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
            "cpu_percent": process.cpu_percent(),
            "threads": process.num_threads()
        }
    except Exception as e:
        logger.error(f"Metrics JSON system error: {e}")
    
    # Database metrics
    try:
        start = time.time()
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM empresas_esg")
        empresas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM profissionais_esg")
        profissionais_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vagas WHERE status='ativa'")
        vagas_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM candidaturas")
        candidaturas_count = cursor.fetchone()[0]
        
        conn.close()
        
        db_response_time = (time.time() - start) * 1000
        
        database = {
            "connected": True,
            "response_time_ms": round(db_response_time, 2),
            "empresas_total": empresas_count,
            "profissionais_total": profissionais_count,
            "vagas_ativas": vagas_count,
            "candidaturas_total": candidaturas_count
        }
    except Exception as e:
        logger.error(f"Metrics JSON database error: {e}")
        database = {
            "connected": False,
            "error": str(e)
        }
    
    # API metrics
    api = {
        "version": Config.APP_VERSION,
        "uptime_seconds": round(time.time() - _start_time, 2),
        "debug_mode": Config.DEBUG,
        "environment": Config.ENVIRONMENT
    }
    
    return MetricsResponse(
        timestamp=datetime.now(),
        system=system,
        database=database,
        api=api
    )
