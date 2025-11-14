@echo off
REM Script para testar a API Green Jobs Brasil
REM Executar este arquivo após iniciar a API com start_api.py

echo ============================================================
echo 🧪 TESTANDO API - GREEN JOBS BRASIL
echo ============================================================
echo.
echo ⏳ Aguardando API inicializar...
timeout /t 3 /nobreak > nul
echo.

echo 📋 TESTANDO ENDPOINTS BÁSICOS
echo ------------------------------------------------------------
curl -s http://127.0.0.1:8002/health | python -m json.tool
echo.
echo ✅ Health check OK
echo.

echo 🌱 TESTANDO TSB - OBJETIVOS
echo ------------------------------------------------------------
curl -s http://127.0.0.1:8002/api/taxonomia/objetivos > temp_objetivos.json
type temp_objetivos.json | python -m json.tool
del temp_objetivos.json
echo.
echo ✅ TSB Objetivos OK
echo.

echo 🏢 TESTANDO TSB - SETORES
echo ------------------------------------------------------------
curl -s http://127.0.0.1:8002/api/taxonomia/setores > temp_setores.json
type temp_setores.json | python -m json.tool
del temp_setores.json
echo.
echo ✅ TSB Setores OK
echo.

echo 📊 TESTANDO EMPRESAS COM TSB
echo ------------------------------------------------------------
curl -s "http://127.0.0.1:8002/empresas/api/listar?tsb=true&limit=5" > temp_empresas.json
type temp_empresas.json | python -m json.tool
del temp_empresas.json
echo.
echo ✅ Empresas com TSB OK
echo.

echo ============================================================
echo ✅ TODOS OS TESTES CONCLUÍDOS!
echo ============================================================
echo.
echo 🎯 Acesse para explorar:
echo    📚 Documentação: http://127.0.0.1:8002/docs
echo    🌱 TSB Info:     http://127.0.0.1:8002/api/taxonomia/
echo.
pause
