@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   ПОВТОРНАЯ ОТПРАВКА ЗАЯВОК
echo ==================================================
echo.
echo Перед запуском рекомендуется остановить backend.
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ОШИБКА] Сначала запустите install_all.bat
    pause
    endlocal & exit /b 1
)
if not exist "backend\.env" (
    echo [ОШИБКА] Сначала запустите configure_email.bat
    pause
    endlocal & exit /b 1
)

".venv\Scripts\python.exe" -m backend.retry_failed_emails
set "EXIT_CODE=%ERRORLEVEL%"
echo.
pause
endlocal & exit /b %EXIT_CODE%
