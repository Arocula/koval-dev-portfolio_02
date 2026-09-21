@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   НАСТРОЙКА ПОЧТЫ GMAIL
echo ==================================================
echo.

where powershell >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] PowerShell не найден.
    echo Скопируйте backend\.env.example в backend\.env и заполните вручную.
    pause
    endlocal & exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\configure_email.ps1" -EnvPath "%~dp0backend\.env"
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
    echo [OK] Настройка завершена. Теперь запустите test_email.bat
) else (
    echo [ОШИБКА] Конфигурация не сохранена.
)
pause
endlocal & exit /b %EXIT_CODE%
