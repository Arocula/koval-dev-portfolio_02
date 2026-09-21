@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

if not exist ".venv\Scripts\python.exe" (
    echo [ОШИБКА] Сначала запустите install_all.bat
    pause
    endlocal & exit /b 1
)

".venv\Scripts\python.exe" -m pytest backend\tests -q
set "EXIT_CODE=%ERRORLEVEL%"
echo.
pause
endlocal & exit /b %EXIT_CODE%
