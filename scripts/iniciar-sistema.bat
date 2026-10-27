@echo off
chcp 65001 > nul
title AeroMotion Dynamics - Inicializador
echo ========================================================
echo   AeroMotion Dynamics - Central de Monitoramento IA
echo ========================================================
echo.

:: Garante que o diretorio atual e a raiz do projeto
cd /d "%~dp0\.."
set PYTHONPATH=%CD%

echo Verificando e liberando portas anteriores se necessario...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do taskkill /f /pid %%a >nul 2>&1

echo [1/2] Iniciando API FastAPI (Porta 8000)...
start "AeroMotion - API" cmd /k "set PYTHONPATH=%CD% && python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak > nul

echo [2/2] Iniciando Dashboard Streamlit (Porta 8501)...
start "AeroMotion - Frontend" cmd /k "set PYTHONPATH=%CD% && python -m streamlit run src/frontend/app.py --server.port 8501"

echo.
echo ========================================================
echo   Servicos iniciados em janelas proprias!
echo   - Raiz do projeto: %CD%
echo   - API:             http://127.0.0.1:8000
echo   - Swagger:         http://127.0.0.1:8000/docs
echo   - Dashboard:       http://127.0.0.1:8501
echo ========================================================
echo.
pause
