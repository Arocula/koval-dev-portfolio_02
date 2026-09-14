from __future__ import annotations

import sys

from backend.config import get_settings
from backend.email_sender import EmailError, EmailSender
from backend.storage import SubmissionStore


def main() -> int:
    settings = get_settings()
    if not settings.email_configured:
        print("[ОШИБКА] SMTP не настроен. Сначала запустите configure_email.bat")
        return 1

    store = SubmissionStore(settings.survey_data_dir)
    records = store.list_by_status({"failed", "timeout"})
    if not records:
        print("[OK] Неотправленных заявок нет.")
        return 0

    sender = EmailSender(settings)
    sent = 0
    failed = 0
    for record in records:
        submission_id = str(record.get("id", "unknown"))
        try:
            sender.send_survey(record)
        except EmailError as exc:
            failed += 1
            store.update_email_status(submission_id, "failed", str(exc))
            print(f"[ОШИБКА] {submission_id}: {exc.public_message}")
        else:
            sent += 1
            store.update_email_status(submission_id, "sent")
            print(f"[OK] {submission_id}: отправлено")

    print(f"\nИтого: отправлено {sent}, ошибок {failed}.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
