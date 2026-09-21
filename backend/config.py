from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
load_dotenv(BACKEND_DIR / ".env", override=False)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "да"}


def _env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} должен быть целым числом") from exc
    return max(minimum, min(maximum, value))


def _env_float(name: str, default: float, minimum: float, maximum: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} должен быть числом") from exc
    return max(minimum, min(maximum, value))


def _env_path(name: str, default: Path) -> Path:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (PROJECT_DIR / path).resolve()


def _cors_origins() -> tuple[str, ...]:
    raw = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    origins = tuple(item.strip().rstrip("/") for item in raw.split(",") if item.strip())
    return origins or ("http://localhost:3000", "http://127.0.0.1:3000")


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "KOVAL_DEV Portfolio API"
    app_env: str = "development"
    cors_origins: tuple[str, ...] = ("http://localhost:3000", "http://127.0.0.1:3000")

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_security: str = "ssl"
    smtp_auth: bool = True
    smtp_username: str = ""
    smtp_password: str = field(default="", repr=False)
    smtp_from_email: str = ""
    smtp_from_name: str = "KOVAL_DEV"
    survey_recipient_email: str = ""
    smtp_timeout_seconds: float = 10.0
    mail_send_timeout_seconds: float = 15.0

    survey_data_dir: Path = BACKEND_DIR / "data" / "submissions"

    @property
    def from_email(self) -> str:
        return self.smtp_from_email or self.smtp_username

    @property
    def recipient_email(self) -> str:
        return self.survey_recipient_email or self.smtp_username

    @property
    def email_configured(self) -> bool:
        base_ready = bool(self.smtp_host and self.smtp_port and self.from_email and self.recipient_email)
        auth_ready = not self.smtp_auth or bool(self.smtp_username and self.smtp_password)
        return base_ready and auth_ready

    @classmethod
    def from_env(cls) -> Settings:
        smtp_timeout = _env_float("SMTP_TIMEOUT_SECONDS", 10.0, 3.0, 60.0)
        mail_timeout = _env_float("MAIL_SEND_TIMEOUT_SECONDS", 15.0, 5.0, 90.0)
        security = os.getenv("SMTP_SECURITY", "ssl").strip().lower()
        if security not in {"ssl", "starttls", "plain"}:
            raise ValueError("SMTP_SECURITY должен быть ssl, starttls или plain")

        return cls(
            app_name=os.getenv("APP_NAME", "KOVAL_DEV Portfolio API").strip(),
            app_env=os.getenv("APP_ENV", "development").strip().lower(),
            cors_origins=_cors_origins(),
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com").strip(),
            smtp_port=_env_int("SMTP_PORT", 465, 1, 65535),
            smtp_security=security,
            smtp_auth=_env_bool("SMTP_AUTH", True),
            smtp_username=os.getenv("SMTP_USERNAME", "").strip(),
            smtp_password=os.getenv("SMTP_PASSWORD", "").strip(),
            smtp_from_email=os.getenv("SMTP_FROM_EMAIL", "").strip(),
            smtp_from_name=os.getenv("SMTP_FROM_NAME", "KOVAL_DEV").strip(),
            survey_recipient_email=os.getenv("SURVEY_RECIPIENT_EMAIL", "").strip(),
            smtp_timeout_seconds=smtp_timeout,
            mail_send_timeout_seconds=max(mail_timeout, smtp_timeout + 2.0),
            survey_data_dir=_env_path(
                "SURVEY_DATA_DIR",
                BACKEND_DIR / "data" / "submissions",
            ),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()
