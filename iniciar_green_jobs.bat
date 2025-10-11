@echo off
title Green Jobs Brasil API
color 0A
echo.
echo ========================================
echo   🌱 GREEN JOBS BRASIL API 🌱
echo ========================================
echo.

REM Ir para o diretório do script
cd /d "%~dp0"

echo ✅ Diretório: %CD%
echo ✅ Verificando arquivos...

REM Verificar se o banco existe
if not exist "gjb_dev.db" (
    echo ❌ Erro: Banco de dados não encontrado!
    echo 📁 Verifique se você está no diretório correto
    pause
    exit /b 1
)

echo ✅ Banco de dados OK
echo ✅ Verificando Python...

"C:\Users\Bruno\AppData\Local\Programs\Python\Python313\python.exe" --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro: Python não encontrado!
    echo 💡 Instale Python ou verifique o caminho
    pause
    exit /b 1
)

echo ✅ Python OK
echo ✅ Iniciando sistema simplificado...
echo.

"C:\Users\Bruno\AppData\Local\Programs\Python\Python313\python.exe" run_green_jobs.py

echo.
echo Sistema encerrado.
pause