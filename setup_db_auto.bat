@echo off
echo Configurando banco PostgreSQL para Green Jobs Brasil...
echo.

REM Definir variável de senha (edite conforme necessário)
set PGPASSWORD=postgres

echo Criando banco de dados gjb_db...
"C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres gjb_db

if %ERRORLEVEL% EQU 0 (
    echo ✅ Banco gjb_db criado com sucesso!
) else (
    echo ⚠️ Banco gjb_db já existe ou erro na criação - continuando...
)

echo.
echo Aplicando schema do banco...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d gjb_db -f "db\schema.sql"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Schema aplicado com sucesso!
) else (
    echo ❌ Erro ao aplicar schema
    pause
    exit /b 1
)

echo.
echo Carregando dados seed dos CNAEs...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d gjb_db -f "db\seed_cnae.sql"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Dados seed carregados com sucesso!
) else (
    echo ❌ Erro ao carregar dados seed
    pause
    exit /b 1
)

echo.
echo ✅ Banco configurado com sucesso!
echo.
pause