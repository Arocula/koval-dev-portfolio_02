@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   ОСТАНОВКА ВСЕХ СЕРВИСОВ
echo ==================================================
echo.

echo Останавливаю все сервисы...

:: Останавливаем по заголовкам окон
taskkill /F /FI "WINDOWTITLE eq KOVAL_DEV Backend*" 2>nul
taskkill /F /FI "WINDOWTITLE eq KOVAL_DEV Frontend*" 2>nul
taskkill /F /FI "WINDOWTITLE eq KOVAL_DEV Flask*" 2>nul

:: Останавливаем по процессам
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

:: Останавливаем процессы на портах
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)

echo.
echo [OK] Все сервисы остановлены.
echo.
pause
endlocal