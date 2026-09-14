@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   БЫСТРЫЙ ЗАПУСК — KOVAL_DEV
echo ==================================================
echo.
echo Запускаю все сервисы без дополнительных проверок...
echo.

:: Запуск Backend
start "KOVAL_DEV Backend" "%ComSpec%" /k "echo FastAPI Backend: http://127.0.0.1:8000 && echo Swagger: http://127.0.0.1:8000/docs && echo. && .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul

:: Запуск Frontend
start "KOVAL_DEV Frontend" "%ComSpec%" /k "cd frontend && echo React Frontend: http://localhost:3000 && echo. && call npm start"
timeout /t 2 /nobreak >nul

:: Запуск Flask
if exist "flask-demo\app.py" (
    start "KOVAL_DEV Flask" "%ComSpec%" /k "cd flask-demo && echo Flask Demo: http://localhost:5000 && echo Админка: http://localhost:5000/admin/login && echo. && call .venv\Scripts\activate && python app.py"
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] Flask Demo не найден
)

echo.
echo ==================================================
echo   ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ
echo ==================================================
echo.
echo 📌 Откройте: http://localhost:3000
echo.
pause