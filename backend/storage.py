from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from backend.schemas import SurveyData

logger = logging.getLogger(__name__)


class SubmissionStore:
    """Хранит каждую заявку отдельным JSON-файлом, чтобы лид не потерялся при сбое SMTP."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def create(self, data: SurveyData) -> dict[str, Any]:
        submission_id = str(uuid4())
        record: dict[str, Any] = {
            "id": submission_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "answers": [answer.model_dump() for answer in data.answers],
            "user_email": str(data.user_email),
            "user_phone": data.user_phone,
            "email_status": "pending",
            "email_error": None,
        }
        with self._lock:
            self._write(record)
        return record

    def update_email_status(self, submission_id: str, status: str, error: str | None = None) -> None:
        path = self._path(submission_id)
        with self._lock:
            if not path.exists():
                logger.warning("Не найдена сохраненная заявка %s", submission_id)
                return
            record = json.loads(path.read_text(encoding="utf-8"))
            record["email_status"] = status
            record["email_error"] = error[:1000] if error else None
            record["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._write(record)

    def get(self, submission_id: str) -> dict[str, Any] | None:
        path = self._path(submission_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_by_status(self, statuses: set[str]) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                logger.exception("Не удалось прочитать сохраненную заявку %s", path)
                continue
            if record.get("email_status") in statuses:
                records.append(record)
        return records

    def _path(self, submission_id: str) -> Path:
        safe_id = "".join(char for char in submission_id if char.isalnum() or char in {"-", "_"})
        return self.directory / f"{safe_id}.json"

    def _write(self, record: dict[str, Any]) -> None:
        path = self._path(str(record["id"]))
        temp_path = path.with_suffix(".tmp")
        temp_path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temp_path, path)
