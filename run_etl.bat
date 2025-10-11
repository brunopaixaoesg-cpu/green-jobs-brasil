@echo off
echo Executando ETL do Green Jobs Brasil...
echo.

cd /d "C:\Users\Bruno\Empresas Verdes"

echo Criando diretórios de dados...
if not exist "data" mkdir data
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed

echo.
echo Executando pipeline ETL...
"C:\Users\Bruno\AppData\Local\Programs\Python\Python313\python.exe" etl\main.py

echo.
echo ✅ ETL executado com sucesso!
echo.
pause