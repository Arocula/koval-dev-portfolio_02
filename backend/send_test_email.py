from __future__ import annotations

import sys
from datetime import datetime, timezone
from uuid import uuid4

from backend.config import get_settings
from backend.email_sender import EmailError, EmailSender


def main() -> int:
    settings = get_settings()
    if not settings.email_configured:
        print("[ОШИБКА] SMTP не настроен. Сначала запустите configure_email.bat")
        return 1

    record = {
        "id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "user_email": settings.smtp_username or settings.from_email,
        "user_phone": "+7 900 000-00-00",
        "answers": [
            {"question": "Проверка почтовой отправки", "answer": "Тестовое письмо доставлено"},
        ],
    }

    try:
        EmailSender(settings).send_survey(record)
    except EmailError as exc:
        print(f"[ОШИБКА] {exc.public_message}")
        return 1

    print(f"[OK] Тестовое письмо отправлено на {settings.recipient_email}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
