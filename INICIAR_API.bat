@echo off
echo ========================================
echo INICIANDO API - Green Jobs Brasil
echo ========================================
echo.

REM Tentar diferentes caminhos do Python
echo Tentando iniciar API...
echo.

REM Tentar python3
where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Usando python3...
    python3 start_api.py
    pause
    goto :end
)

REM Tentar py
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Usando py launcher...
    py start_api.py
    pause
    goto :end
)

REM Tentar python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Usando python...
    python start_api.py
    pause
    goto :end
)

echo.
echo ❌ ERRO: Python não encontrado!
echo.
echo Por favor, execute manualmente no terminal que funciona:
echo     python start_api.py
echo.
echo Ou verifique se o Python está instalado:
echo     python --version
echo.
pause

:end
