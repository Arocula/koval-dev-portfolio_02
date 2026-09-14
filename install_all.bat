@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   УСТАНОВКА ЗАВИСИМОСТЕЙ — KOVAL_DEV
echo ==================================================
echo.

call :find_python
if errorlevel 1 goto :python_error
%PYTHON_EXE% %PYTHON_ARGS% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 goto :python_version_error

where node >nul 2>&1
if errorlevel 1 goto :node_error
where npm >nul 2>&1
if errorlevel 1 goto :node_error
node -e "process.exit(Number(process.versions.node.split('.')[0]) >= 18 ? 0 : 1)"
if errorlevel 1 goto :node_version_error

echo [1/4] Создание Python-окружения...
if not exist ".venv\Scripts\python.exe" (
    %PYTHON_EXE% %PYTHON_ARGS% -m venv .venv
    if errorlevel 1 goto :install_error
) else (
    echo [OK] .venv уже существует
)
echo.

echo [2/4] Установка backend-зависимостей...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :install_error
".venv\Scripts\python.exe" -m pip install -r "backend\requirements-dev.txt"
if errorlevel 1 goto :install_error
echo [OK] Backend готов
echo.

echo [3/4] Установка frontend-зависимостей...
pushd "frontend"
if exist "package-lock.json" (
    call npm ci
) else (
    call npm install
)
if errorlevel 1 (
    popd
    goto :install_error
)
popd
echo [OK] Frontend готов
echo.

echo [4/4] Подготовка конфигурации...
if not exist "backend\.env" (
    copy /Y "backend\.env.example" "backend\.env" >nul
    echo [ВНИМАНИЕ] Создан backend\.env без пароля почты.
    echo             Запустите configure_email.bat перед проверкой формы.
) else (
    echo [OK] backend\.env уже существует
)

:: Установка Flask зависимостей если есть
if exist "flask-demo\requirements.txt" (
    echo.
    echo [5/5] Установка Flask зависимостей...
    if not exist "flask-demo\.venv\Scripts\python.exe" (
        cd flask-demo
        python -m venv .venv
        call .venv\Scripts\activate
        pip install -r requirements.txt
        cd ..
    ) else (
        echo [OK] Flask окружение готово
    )
)

echo.
echo ==================================================
echo   УСТАНОВКА ЗАВЕРШЕНА
echo ==================================================
echo.
echo 🚀 Запуск всех сервисов: run_all.bat
echo 🚀 Быстрый запуск: run_all_quick.bat
echo 📧 Настройка почты: configure_email.bat
echo.
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

:python_error
echo [ОШИБКА] Python 3 не найден.
echo Установите Python 3.10+ и включите опцию Add Python to PATH.
if not defined NO_PAUSE pause
endlocal & exit /b 1

:python_version_error
echo [ОШИБКА] Установленная версия Python слишком старая.
echo Нужен Python 3.10 или новее.
if not defined NO_PAUSE pause
endlocal & exit /b 1

:node_error
echo [ОШИБКА] Node.js или npm не найдены.
echo Установите Node.js 18 или новее.
if not defined NO_PAUSE pause
endlocal & exit /b 1

:node_version_error
echo [ОШИБКА] Установленная версия Node.js слишком старая.
echo Нужен Node.js 18 или новее.
if not defined NO_PAUSE pause
endlocal & exit /b 1

:install_error
echo.
echo [ОШИБКА] Установка прервана. Смотрите сообщение выше.
if not defined NO_PAUSE pause
endlocal & exit /b 1