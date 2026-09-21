# KOVAL_DEV — React + FastAPI

Исправленная версия существующего проекта без Docker. Backend и frontend запускаются обычными `.bat`-файлами в Windows.

## Что исправлено

Главная проблема была в почтовой отправке:

- в старом `email_sender.py` находилась незакрытая строка, из-за которой модуль не мог нормально загрузиться;
- пароль Gmail был записан прямо в исходном коде;
- номер телефона принимался API, но не добавлялся в письмо;
- блокирующий `smtplib` запускался непосредственно внутри `async`-эндпоинта FastAPI;
- frontend не ограничивал время `fetch`, поэтому кнопка могла бесконечно показывать «Отправка...»;
- ошибки backend скрывались за общим `alert` без понятной причины.

Теперь:

- SMTP настраивается через `backend/.env`;
- пароль приложения не хранится в исходниках;
- письмо содержит email, телефон и все ответы пользователя;
- отправка SMTP выполняется в отдельном потоке;
- backend ограничивает время отправки, frontend — время ожидания ответа;
- пользователь получает понятную ошибку вместо зависшей загрузки;
- каждая заявка сначала сохраняется в `backend/data/submissions`, поэтому контакт не теряется при временном сбое почты;
- добавлены валидация email/телефона, honeypot-антиспам, healthcheck и 10 тестов;
- исправлены CORS и Vite proxy;
- удалён дублирующий frontend-entrypoint и старый тяжёлый сборщик заменён на Vite 6;
- исправлена логика интерактивного BIOS-раздела;
- заполнены разделы портфолио и добавлена адаптивная верстка.

## Важное действие по безопасности

В исходном архиве пароль приложения Gmail был открыт в `backend/email_sender.py`. Его необходимо отозвать в аккаунте Google и создать новый пароль приложения. Старый пароль в исправленный проект не перенесён.

## Первый запуск в Windows

### 1. Проверить систему

Запустите:

```text
check_system.bat
```

Нужны:

- Python 3.10 или новее;
- Node.js 18 или новее;
- npm;
- PowerShell для удобной настройки почты.

### 2. Установить зависимости

```text
install_all.bat
```

Файл проверит версии Python/Node.js, создаст `.venv`, установит зафиксированные backend-зависимости и выполнит воспроизводимый `npm ci` для frontend.

### 3. Настроить Gmail

```text
configure_email.bat
```

Скрипт запросит:

- Gmail отправителя;
- адрес, на который должны приходить заявки;
- новый пароль приложения Google.

Пароль при вводе не отображается. Настройки сохраняются только локально в `backend/.env`.

После изменения `.env` перезапустите backend.

### 4. Проверить реальную отправку

```text
test_email.bat
```

На указанный адрес должно прийти тестовое письмо.

### 5. Запустить проект

```text
start_all.bat
```

Откроются два окна терминала:

- FastAPI backend;
- React frontend.

Адреса:

```text
Frontend: http://localhost:3000
Backend:  http://127.0.0.1:8000
Swagger:  http://127.0.0.1:8000/docs
Health:   http://127.0.0.1:8000/api/health
```

## Отдельный запуск

```text
run_backend.bat
run_frontend.bat
```

## Проверки

Backend-тесты:

```text
test_backend.bat
```

Набор включает проверку успешной отправки, ошибок SMTP, валидации, антиспама, сохранения заявки и принудительного завершения зависшего ожидания по таймауту.

Production-сборка React:

```text
build_frontend.bat
```

Готовая сборка появится в `frontend/dist`.

Повторная отправка заявок, которые сохранились со статусом `failed` или `timeout`:

```text
retry_failed_emails.bat
```

Перед повторной отправкой лучше остановить backend.

## Почтовая конфигурация

Пример находится в `backend/.env.example`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_SECURITY=ssl
SMTP_AUTH=true
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-google-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=KOVAL_DEV
SURVEY_RECIPIENT_EMAIL=your-email@gmail.com
SMTP_TIMEOUT_SECONDS=10
MAIL_SEND_TIMEOUT_SECONDS=15
```

Для Gmail нужен именно пароль приложения, а не обычный пароль аккаунта.

## Что происходит при отправке опроса

1. React проверяет форму и отправляет `POST /api/survey`.
2. FastAPI валидирует email, телефон и ответы.
3. Заявка сохраняется отдельным JSON-файлом.
4. SMTP запускается в отдельном рабочем потоке.
5. После подтверждённой доставки API возвращает `201 Created`.
6. При ошибке API возвращает понятный код и прекращает ожидание; заявка остаётся сохранённой локально.

Пример запроса:

```json
{
  "answers": [
    {
      "question": "Какой сайт нужен?",
      "answer": "Лендинг"
    }
  ],
  "user_email": "client@example.com",
  "user_phone": "+7 999 123-45-67",
  "website": ""
}
```

## Результаты финальной проверки

- чистая установка Python-зависимостей на Python 3.13;
- `10 passed` для backend-тестов;
- Ruff и `compileall` без ошибок;
- production-сборка React/Vite без ошибок;
- `npm audit`: 0 известных уязвимостей;
- совместный запуск frontend + backend и proxy `/api` проверены;
- заявка при недоступной почте возвращает ошибку без вечной загрузки и остаётся в локальном хранилище.

Реальную доставку через конкретный Gmail нужно один раз подтвердить на вашем компьютере командой `test_email.bat`, поскольку новый пароль приложения намеренно не включён в архив.

## Структура

```text
SitePortfolio_fixed/
├── backend/
│   ├── main.py              # FastAPI и маршруты
│   ├── config.py            # настройки из .env
│   ├── schemas.py           # Pydantic-валидация
│   ├── email_sender.py      # SMTP и HTML/текстовое письмо
│   ├── storage.py           # резервное сохранение заявок
│   ├── send_test_email.py   # ручная проверка SMTP
│   ├── retry_failed_emails.py # повторная отправка сбоев
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── src/
│   │   ├── components/HomePage.jsx
│   │   ├── data/questions.js
│   │   ├── services/surveyApi.js
│   │   ├── App.jsx
│   │   ├── app.css
│   │   └── main.jsx
│   ├── package.json
│   └── package-lock.json
├── scripts/configure_email.ps1
├── install_all.bat
├── configure_email.bat
├── test_email.bat
├── retry_failed_emails.bat
├── start_all.bat
├── run_backend.bat
└── run_frontend.bat
```

## Если письмо не приходит

1. Откройте `http://127.0.0.1:8000/api/health`. Поле `email_configured` должно быть `true`.
2. Запустите `test_email.bat` и прочитайте точную ошибку в окне.
3. Убедитесь, что используется новый пароль приложения Google.
4. Перезапустите backend после изменения `backend/.env`.
5. Проверьте папки «Спам» и «Промоакции».
6. Убедитесь, что антивирус или сеть не блокируют исходящее соединение с `smtp.gmail.com:465`.

Неотправленные заявки можно повторно отправить через `retry_failed_emails.bat`.

Сохранённые заявки находятся в:

```text
backend/data/submissions/
```
