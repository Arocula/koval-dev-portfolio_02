@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

if not exist "frontend\node_modules\" (
    echo [ОШИБКА] Сначала запустите install_all.bat
    pause
    endlocal & exit /b 1
)

pushd "frontend"
call npm run build
set "EXIT_CODE=%ERRORLEVEL%"
popd

echo.
if "%EXIT_CODE%"=="0" echo [OK] Сборка создана в frontend\dist
pause
endlocal & exit /b %EXIT_CODE%
