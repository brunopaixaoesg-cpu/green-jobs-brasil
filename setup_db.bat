@echo off
echo Configurando banco PostgreSQL para Green Jobs Brasil...
echo.

REM Criar o banco de dados
echo Criando banco de dados gjb_db...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE gjb_db;"

echo.
echo Aplicando schema do banco...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d gjb_db -f "db\schema.sql"

echo.
echo Carregando dados seed dos CNAEs...
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d gjb_db -f "db\seed_cnae.sql"

echo.
echo ✅ Banco configurado com sucesso!
echo.
pause