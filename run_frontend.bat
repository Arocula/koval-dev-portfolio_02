@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   REACT FRONTEND
echo ==================================================
echo.

where npm >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] npm не найден. Установите Node.js.
    pause
    endlocal & exit /b 1
)

if not exist "frontend\node_modules\" (
    echo [ОШИБКА] Не найдены frontend-зависимости.
    echo Сначала запустите install_all.bat
    pause
    endlocal & exit /b 1
)

pushd "frontend"
echo Frontend: http://localhost:3000
echo Для остановки нажмите Ctrl+C.
echo.
call npm start
set "EXIT_CODE=%ERRORLEVEL%"
popd

echo.
if not "%EXIT_CODE%"=="0" echo [ОШИБКА] Frontend завершился с кодом %EXIT_CODE%.
pause
endlocal & exit /b %EXIT_CODE%
