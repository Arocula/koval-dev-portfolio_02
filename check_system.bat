@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   ПРОВЕРКА СИСТЕМЫ — KOVAL_DEV
echo ==================================================
echo.

set "HAS_ERROR=0"

echo [1/4] Python 3.10+
call :find_python
if errorlevel 1 (
    echo [ОШИБКА] Python не найден. Установите Python 3.10 или новее.
    set "HAS_ERROR=1"
) else (
    %PYTHON_EXE% %PYTHON_ARGS% --version
    %PYTHON_EXE% %PYTHON_ARGS% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
    if errorlevel 1 (
        echo [ОШИБКА] Нужен Python 3.10 или новее.
        set "HAS_ERROR=1"
    ) else (
        echo [OK] Версия Python подходит
    )
)
echo.

echo [2/4] Node.js 18+
where node >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Node.js не найден. Установите Node.js 18 или новее.
    set "HAS_ERROR=1"
) else (
    node --version
    node -e "process.exit(Number(process.versions.node.split('.')[0]) >= 18 ? 0 : 1)"
    if errorlevel 1 (
        echo [ОШИБКА] Нужен Node.js 18 или новее.
        set "HAS_ERROR=1"
    ) else (
        echo [OK] Версия Node.js подходит
    )
)
echo.

echo [3/4] npm
where npm >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] npm не найден. Он устанавливается вместе с Node.js.
    set "HAS_ERROR=1"
) else (
    call npm --version
    echo [OK] npm найден
)
echo.

echo [4/4] PowerShell
where powershell >nul 2>&1
if errorlevel 1 (
    echo [ПРЕДУПРЕЖДЕНИЕ] PowerShell не найден.
    echo configure_email.bat будет недоступен, но backend\.env можно заполнить вручную.
) else (
    echo [OK] PowerShell найден
)
echo.

if "%HAS_ERROR%"=="1" (
    echo Проверка завершена с ошибками.
    if not defined NO_PAUSE pause
    endlocal & exit /b 1
)

echo [OK] Система готова к установке проекта.
if not defined NO_PAUSE pause
endlocal & exit /b 0

:find_python
where py >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=py"
    set "PYTHON_ARGS=-3"
    exit /b 0
)
where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    set "PYTHON_ARGS="
    exit /b 0
)
exit /b 1
