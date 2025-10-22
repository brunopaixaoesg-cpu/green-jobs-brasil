@echo off
echo ========================================
echo GREEN JOBS BRASIL - CONFIGURAR FIREWALL
echo ========================================
echo.
echo Este script vai liberar a porta 8002 no firewall
echo para permitir acesso via rede local (celular)
echo.
pause

REM Verificar se esta rodando como administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Executando como Administrador
    echo.
    echo Liberando porta 8002...
    netsh advfirewall firewall add rule name="Green Jobs Brasil API" dir=in action=allow protocol=TCP localport=8002
    echo.
    echo [SUCESSO] Porta 8002 liberada!
    echo.
    echo Agora voce pode executar: py start_mobile.py
    echo.
    pause
) else (
    echo [ERRO] Este script precisa ser executado como Administrador!
    echo.
    echo Como fazer:
    echo 1. Clique com botao direito neste arquivo
    echo 2. Selecione "Executar como administrador"
    echo.
    pause
)
