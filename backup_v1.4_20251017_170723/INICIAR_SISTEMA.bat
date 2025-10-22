@echo off
echo ========================================
echo   GREEN JOBS BRASIL - Sistema v1.3
echo   Sistema de Autenticacao JWT
echo ========================================
echo.
echo Iniciando servidor...
echo.
echo Login: http://127.0.0.1:8002/login
echo Dashboard: http://127.0.0.1:8002/dashboard
echo API: http://127.0.0.1:8002
echo Docs: http://127.0.0.1:8002/docs
echo.
echo Credenciais do Usuario:
echo   Email: bruno@greenjobsbrasil.com.br
echo   Senha: Senha123!
echo.
echo Credenciais do Admin:
echo   Email: admin@greenjobs.com.br
echo   Senha: admin123
echo.
echo Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

cd /d "C:\Users\Bruno\Empresas Verdes"
py start_api.py

pause
