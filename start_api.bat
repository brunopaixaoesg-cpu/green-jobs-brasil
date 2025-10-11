@echo off
echo Iniciando Green Jobs Brasil API...
cd /d "C:\Users\Bruno\Empresas Verdes\api"
echo API será iniciada em http://localhost:8000
echo Documentação disponível em http://localhost:8000/docs
echo.
"C:\Users\Bruno\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause