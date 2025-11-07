"""
Teste do Sistema de Logging Estruturado P3.3
Demonstra as funcionalidades do novo logging_config
"""
import sys
import os
import time

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.logging_config import logger, log_request, log_db_query, log_error, log_metric

def test_basic_logging():
    """Testa níveis básicos de log"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Níveis Básicos de Log")
    print("=" * 60)
    
    logger.debug("Mensagem DEBUG - detalhes técnicos")
    logger.info("Mensagem INFO - informação geral")
    logger.warning("Mensagem WARNING - atenção necessária")
    logger.error("Mensagem ERROR - algo deu errado")
    
    print("✅ Logs básicos enviados\n")


def test_http_logging():
    """Testa logging de requisições HTTP"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: Logging de Requisições HTTP")
    print("=" * 60)
    
    # Request bem-sucedido
    log_request("GET", "/api/profissionais", 200, 45.5)
    
    # Request com erro do cliente
    log_request("POST", "/api/candidaturas", 400, 12.3)
    
    # Request com erro do servidor
    log_request("GET", "/api/empresas/123", 500, 234.7)
    
    # Request rápido
    log_request("GET", "/health", 200, 2.1)
    
    print("✅ Logs HTTP estruturados enviados\n")


def test_db_logging():
    """Testa logging de queries de banco"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: Logging de Queries de Banco")
    print("=" * 60)
    
    # Query rápida
    log_db_query(
        "SELECT * FROM profissionais_esg WHERE id = ?",
        duration_ms=5.2,
        rows_affected=1
    )
    
    # Query lenta (slow query warning)
    log_db_query(
        "SELECT * FROM candidaturas JOIN vagas ON candidaturas.vaga_id = vagas.id WHERE status = 'ativa'",
        duration_ms=1234.5,
        rows_affected=857
    )
    
    # Query muito longa (deve truncar)
    long_query = "SELECT " + ", ".join([f"campo_{i}" for i in range(50)]) + " FROM tabela_muito_grande WHERE condicao = 1"
    log_db_query(long_query, duration_ms=89.3, rows_affected=1000)
    
    print("✅ Logs de DB estruturados enviados\n")


def test_error_logging():
    """Testa logging de erros"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: Logging de Erros")
    print("=" * 60)
    
    # Erro simples
    try:
        resultado = 10 / 0
    except ZeroDivisionError as e:
        log_error(e, context={"operacao": "divisao", "numerador": 10, "denominador": 0})
    
    # Erro com contexto
    try:
        raise ValueError("CNPJ inválido: formato incorreto")
    except ValueError as e:
        log_error(e, context={"cnpj": "12.345.678/0001-99", "endpoint": "/api/empresas"})
    
    print("✅ Logs de erro estruturados enviados\n")


def test_metric_logging():
    """Testa logging de métricas"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Logging de Métricas")
    print("=" * 60)
    
    # Métrica de performance
    log_metric("api_response_time", 45.7, unit="ms", tags={"endpoint": "/api/profissionais"})
    
    # Métrica de negócio
    log_metric("candidaturas_criadas", 15, unit="count", tags={"periodo": "hoje"})
    
    # Métrica de sistema
    log_metric("memory_usage", 234.5, unit="MB")
    
    # Métrica de matching
    log_metric("score_medio_matching", 47.4, unit="%", tags={"algoritmo": "ml_v3"})
    
    print("✅ Logs de métricas estruturados enviados\n")


def test_json_format():
    """Testa formato JSON (se configurado)"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Verificação de Formato")
    print("=" * 60)
    
    from api.config import Config
    
    print(f"Formato de log configurado: {Config.LOG_FORMAT}")
    print(f"Nível de log: {Config.LOG_LEVEL}")
    print(f"Arquivo de log: {Config.get_log_path()}")
    print(f"Tamanho máximo: {Config.LOG_MAX_SIZE_MB}MB")
    print(f"Backups: {Config.LOG_BACKUP_COUNT}")
    
    if Config.LOG_FORMAT == "json":
        print("\n✅ Logs serão salvos em formato JSON (produção)")
    else:
        print("\n✅ Logs serão salvos em formato TEXT (desenvolvimento)")
    
    print()


def test_log_rotation():
    """Simula escrita de logs para testar rotation"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 7: Simulação de Log Rotation")
    print("=" * 60)
    
    print("Escrevendo 100 mensagens de log para testar rotation...")
    
    for i in range(100):
        logger.info(f"Mensagem de teste {i+1}/100 - simulando carga de produção")
        
        if (i + 1) % 25 == 0:
            print(f"  ✓ {i+1} mensagens escritas")
    
    print("\n✅ Rotation testado (verifique o diretório logs/)\n")


def test_performance():
    """Testa performance do logging"""
    print("\n" + "=" * 60)
    print("🧪 TESTE 8: Performance de Logging")
    print("=" * 60)
    
    iterations = 1000
    
    # Testar performance de logs básicos
    start = time.time()
    for i in range(iterations):
        logger.info(f"Performance test iteration {i}")
    basic_duration = (time.time() - start) * 1000
    
    # Testar performance de logs estruturados
    start = time.time()
    for i in range(iterations):
        log_request("GET", f"/api/test/{i}", 200, 10.5)
    structured_duration = (time.time() - start) * 1000
    
    print(f"Logs básicos: {iterations} em {basic_duration:.2f}ms ({basic_duration/iterations:.3f}ms/log)")
    print(f"Logs estruturados: {iterations} em {structured_duration:.2f}ms ({structured_duration/iterations:.3f}ms/log)")
    
    if structured_duration < 1000:  # Menos de 1 segundo para 1000 logs
        print("\n✅ Performance aceitável para produção\n")
    else:
        print("\n⚠️  Performance pode precisar de otimização\n")


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🌿 GREEN JOBS BRASIL - TESTE DE LOGGING P3.3")
    print("=" * 60)
    
    try:
        test_basic_logging()
        test_http_logging()
        test_db_logging()
        test_error_logging()
        test_metric_logging()
        test_json_format()
        test_log_rotation()
        test_performance()
        
        print("=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        
        print("\n📁 Verifique os arquivos de log em:")
        from api.config import Config
        print(f"   {Config.get_log_path()}")
        print(f"   {Config.get_log_path()}.1 (backup 1)")
        print(f"   {Config.get_log_path()}.2 (backup 2)")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
