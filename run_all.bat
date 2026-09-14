@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
cls

echo ==================================================
echo   ЗАПУСК ВСЕХ СИСТЕМ — KOVAL_DEV
echo ==================================================
echo.
echo Будут запущены:
echo   🔹 Установка зависимостей (если нужно)
echo   🔹 Настройка почты (если нужно)
echo   🔹 Проверка системы
echo   🔹 Backend FastAPI
echo   🔹 Frontend React
echo   🔹 Flask Demo
echo   🔹 Тестирование почты
echo.
echo ==================================================
echo.

:: ============================================
:: ШАГ 1: Проверка системы
:: ============================================
echo [1/7] Проверка системы...
if exist "check_system.bat" (
    call check_system.bat
    if errorlevel 1 (
        echo [ОШИБКА] Система не соответствует требованиям
        pause
        endlocal & exit /b 1
    )
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] check_system.bat не найден
)
echo.

:: ============================================
:: ШАГ 2: Установка зависимостей
:: ============================================
echo [2/7] Проверка и установка зависимостей...
if not exist ".venv\Scripts\python.exe" (
    echo Установка Python зависимостей...
    if exist "install_all.bat" (
        call install_all.bat
        if errorlevel 1 (
            echo [ОШИБКА] Не удалось установить зависимости
            pause
            endlocal & exit /b 1
        )
    ) else (
        echo [ОШИБКА] install_all.bat не найден
        pause
        endlocal & exit /b 1
    )
) else (
    echo [OK] Зависимости уже установлены
)
echo.

:: ============================================
:: ШАГ 3: Настройка почты (проверка .env)
:: ============================================
echo [3/7] Проверка настройки почты...
if not exist "backend\.env" (
    echo [ПРЕДУПРЕЖДЕНИЕ] Почта не настроена!
    echo Запускаю configure_email.bat...
    if exist "configure_email.bat" (
        call configure_email.bat
        if errorlevel 1 (
            echo [ПРЕДУПРЕЖДЕНИЕ] Настройка почты прервана или не завершена
            echo Продолжаю без почты...
        )
    ) else (
        echo [ПРЕДУПРЕЖДЕНИЕ] configure_email.bat не найден
        echo Создайте backend/.env вручную
    )
) else (
    echo [OK] Почта настроена
)
echo.

:: ============================================
:: ШАГ 4: Проверка Flask демо
:: ============================================
echo [4/7] Подготовка Flask Demo...
if exist "flask-demo\app.py" (
    if not exist "flask-demo\.venv\Scripts\python.exe" (
        echo Устанавливаю зависимости для Flask...
        cd flask-demo
        python -m venv .venv
        call .venv\Scripts\activate
        pip install -r requirements.txt
        cd ..
    ) else (
        echo [OK] Flask окружение готово
    )
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] Flask Demo не найден (flask-demo/app.py)
)
echo.

:: ============================================
:: ШАГ 5: Проверка отправки почты
:: ============================================
echo [5/7] Проверка отправки почты...
if exist "test_email.bat" (
    echo Запускаю тест почты...
    call test_email.bat
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] test_email.bat не найден
)
echo.

:: ============================================
:: ШАГ 6: Сборка фронтенда (опционально)
:: ============================================
echo [6/7] Сборка фронтенда для production...
if exist "build_frontend.bat" (
    echo Запускаю сборку фронтенда...
    call build_frontend.bat
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] build_frontend.bat не найден
    echo Пропускаю сборку...
)
echo.

:: ============================================
:: ШАГ 7: Запуск всех сервисов
:: ============================================
echo [7/7] Запуск всех сервисов...
echo.

if exist "start_all_services.bat" (
    call start_all_services.bat
) else (
    echo [ОШИБКА] start_all_services.bat не найден!
    echo Создаю его автоматически...
    
    :: Создаем start_all_services.bat если его нет
    (
        echo @echo off
        echo setlocal EnableExtensions
        echo chcp 65001 ^>nul
        echo cd /d "%%~dp0"
        echo cls
        echo.
        echo echo ==================================================
        echo echo   ЗАПУСК ВСЕХ СЕРВИСОВ — KOVAL_DEV
        echo echo ==================================================
        echo echo.
        echo.
        echo :: Запуск Backend
        echo echo [1/3] Запуск FastAPI Backend...
        echo start "KOVAL_DEV Backend" "%%ComSpec%%" /k "echo FastAPI Backend: http://127.0.0.1:8000 ^&^& echo Swagger: http://127.0.0.1:8000/docs ^&^& echo. ^&^& .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
        echo timeout /t 2 /nobreak ^>nul
        echo.
        echo :: Запуск Frontend
        echo echo [2/3] Запуск React Frontend...
        echo start "KOVAL_DEV Frontend" "%%ComSpec%%" /k "cd frontend ^&^& echo React Frontend: http://localhost:3000 ^&^& echo. ^&^& call npm start"
        echo timeout /t 2 /nobreak ^>nul
        echo.
        echo :: Запуск Flask
        echo echo [3/3] Запуск Flask Demo...
        echo if exist "flask-demo\app.py" (
        echo     start "KOVAL_DEV Flask" "%%ComSpec%%" /k "cd flask-demo ^&^& echo Flask Demo: http://localhost:5000 ^&^& echo. ^&^& call .venv\Scripts\activate ^&^& python app.py"
        echo ) else (
        echo     echo [ПРЕДУПРЕЖДЕНИЕ] Flask Demo пропущен
        echo )
        echo.
        echo echo.
        echo echo ==================================================
        echo echo   ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ
        echo echo ==================================================
        echo echo.
        echo echo 📌 Откройте: http://localhost:3000
        echo echo.
        echo pause
    ) > start_all_services.bat
    
    echo [OK] Создан start_all_services.bat
    echo Запускаю его...
    call start_all_services.bat
)

echo.
echo ==================================================
echo   ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ
echo ==================================================
echo.
echo 📌 Откройте браузер: http://localhost:3000
echo.
echo 📋 Доступные сервисы:
echo    🔹 React Frontend : http://localhost:3000
echo    🔹 FastAPI Backend: http://127.0.0.1:8000
echo    🔹 Swagger API    : http://127.0.0.1:8000/docs
if exist "flask-demo\app.py" (
    echo    🔹 Flask Demo     : http://localhost:5000
    echo    🔹 Flask Admin    : http://localhost:5000/admin/login
)
echo.
echo 🔄 Для остановки всех сервисов нажмите Ctrl+C в каждом окне
echo    или запустите stop_all_services.bat
echo.
pause
endlocal