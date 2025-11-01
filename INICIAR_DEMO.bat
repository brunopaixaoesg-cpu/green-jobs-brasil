@echo off
echo ========================================
echo   GREEN JOBS BRASIL - SISTEMA ESG
echo        Inicializacao para Demo
echo ========================================
echo.

echo [1/3] Verificando Python...
py --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.13+ antes de continuar
    pause
    exit /b 1
)

echo [2/3] Verificando banco de dados...
if not exist "api\gjb_dev.db" (
    echo Populando banco com dados de exemplo...
    py popular_profissionais_completo.py
)

echo [3/3] Iniciando Green Jobs Brasil API...
echo.
echo ==========================================
echo  ACESSE NO NAVEGADOR:
echo  http://127.0.0.1:8002/vagas
echo  http://127.0.0.1:8002/dashboard_empresa/1
echo  http://127.0.0.1:8002/teste_sistema
echo ==========================================
echo.
echo Pressione Ctrl+C para parar o sistema
echo.

py start_api.py

pause