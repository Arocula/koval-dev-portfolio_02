@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   ЗАПУСК KOVAL_DEV — REACT + FASTAPI
echo ==================================================
echo.

if not exist ".venv\Scripts\python.exe" goto :install
if not exist "frontend\node_modules\" goto :install
goto :start

:install
echo Зависимости еще не установлены. Запускаю установку...
set "NO_PAUSE=1"
call "%~dp0install_all.bat"
set "NO_PAUSE="
if errorlevel 1 (
    echo [ОШИБКА] Не удалось подготовить проект.
    pause
    endlocal & exit /b 1
)

:start
echo Запускаю backend в отдельном окне...
start "KOVAL_DEV Backend" "%ComSpec%" /k call "%~dp0run_backend.bat"

timeout /t 2 /nobreak >nul

echo Запускаю frontend в отдельном окне...
start "KOVAL_DEV Frontend" "%ComSpec%" /k call "%~dp0run_frontend.bat"

echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo Swagger:  http://127.0.0.1:8000/docs
echo.
echo Серверы работают в двух открывшихся окнах.
echo Для остановки нажмите Ctrl+C в каждом окне.
echo.
pause
endlocal
