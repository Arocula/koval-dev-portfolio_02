@echo off
cd /d "%~dp0flask-demo"
echo ==================================================
echo   ЗАПУСК FLASK ДЕМО
echo ==================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Создаю виртуальное окружение...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
)

call .venv\Scripts\activate
echo Flask демо: http://localhost:5000
echo Админка: http://localhost:5000/admin/login
echo.
python app.py
pause