@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   FASTAPI BACKEND
echo ==================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ОШИБКА] Не найдено виртуальное окружение .venv
    echo Сначала запустите install_all.bat
    pause
    endlocal & exit /b 1
)

if not exist "backend\.env" (
    echo [ПРЕДУПРЕЖДЕНИЕ] backend\.env не найден.
    echo Почтовая отправка будет недоступна до запуска configure_email.bat
    echo.
)

echo Backend: http://127.0.0.1:8000
echo Swagger: http://127.0.0.1:8000/docs
echo Проверка: http://127.0.0.1:8000/api/health
echo Для остановки нажмите Ctrl+C.
echo.

".venv\Scripts\python.exe" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if not "%EXIT_CODE%"=="0" echo [ОШИБКА] Backend завершился с кодом %EXIT_CODE%.
pause
endlocal & exit /b %EXIT_CODE%
