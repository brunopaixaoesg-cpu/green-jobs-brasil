@echo off
echo ========================================
echo REINICIANDO API E TESTANDO KPIs
echo ========================================
echo.

echo [1/3] Parando API anterior...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *start_api*" 2>nul
timeout /t 2 >nul

echo.
echo [2/3] Iniciando API na porta 8002...
start "Green Jobs API" python start_api.py

echo.
echo [3/3] Aguardando API inicializar (10 segundos)...
timeout /t 10

echo.
echo ========================================
echo TESTANDO ENDPOINT /api/kpis/gerais
echo ========================================
curl http://127.0.0.1:8002/api/kpis/gerais

echo.
echo.
echo ========================================
echo TESTANDO ENDPOINT /api/kpis/
echo ========================================
curl "http://127.0.0.1:8002/api/kpis/?periodo=mes&limit_top=5"

echo.
echo.
echo ========================================
echo Para executar teste completo:
echo     python tests/teste_kpis.py
echo ========================================
pause
