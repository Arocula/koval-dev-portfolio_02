param(
    [Parameter(Mandatory = $true)]
    [string]$EnvPath
)

$ErrorActionPreference = 'Stop'

function Read-ValidEmail([string]$Prompt) {
    while ($true) {
        $value = (Read-Host $Prompt).Trim()
        if ($value -match '^[^\s@]+@[^\s@]+\.[^\s@]+$') {
            return $value
        }
        Write-Host 'Введите корректный email.' -ForegroundColor Yellow
    }
}

if (Test-Path -LiteralPath $EnvPath) {
    $answer = (Read-Host 'backend/.env уже существует. Перезаписать? [y/N]').Trim().ToLowerInvariant()
    if ($answer -notin @('y', 'yes', 'д', 'да')) {
        Write-Host 'Настройка отменена.'
        exit 0
    }
}

Write-Host 'Используйте пароль приложения Google из 16 символов, не пароль аккаунта.' -ForegroundColor Cyan
Write-Host ''

$sender = Read-ValidEmail 'Gmail отправителя'
$recipientInput = (Read-Host 'Куда отправлять заявки (Enter = тот же адрес)').Trim()
$recipient = if ([string]::IsNullOrWhiteSpace($recipientInput)) { $sender } else { $recipientInput }
if ($recipient -notmatch '^[^\s@]+@[^\s@]+\.[^\s@]+$') {
    throw 'Некорректный email получателя.'
}

$securePassword = Read-Host 'Пароль приложения Google' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
try {
    $password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
}
$password = $password -replace '\s', ''
if ([string]::IsNullOrWhiteSpace($password)) {
    throw 'Пароль приложения не может быть пустым.'
}

$lines = @(
    'APP_ENV=development',
    'CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000',
    '',
    'SMTP_HOST=smtp.gmail.com',
    'SMTP_PORT=465',
    'SMTP_SECURITY=ssl',
    'SMTP_AUTH=true',
    "SMTP_USERNAME=$sender",
    "SMTP_PASSWORD=$password",
    "SMTP_FROM_EMAIL=$sender",
    'SMTP_FROM_NAME=KOVAL_DEV',
    "SURVEY_RECIPIENT_EMAIL=$recipient",
    'SMTP_TIMEOUT_SECONDS=10',
    'MAIL_SEND_TIMEOUT_SECONDS=15',
    '',
    'SURVEY_DATA_DIR=backend/data/submissions'
)

$directory = Split-Path -Parent $EnvPath
[IO.Directory]::CreateDirectory($directory) | Out-Null
[IO.File]::WriteAllLines($EnvPath, $lines, [Text.UTF8Encoding]::new($false))
Write-Host "Конфигурация сохранена: $EnvPath" -ForegroundColor Green
