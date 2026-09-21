from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path

from fastapi.testclient import TestClient

from backend.config import Settings
from backend.email_sender import EmailDeliveryError
from backend.main import create_app
from backend.schemas import SurveyData
from backend.storage import SubmissionStore


class SlowEmailSender:
    def __init__(self, delay_seconds: float):
        self.delay_seconds = delay_seconds

    def send_survey(self, record: dict) -> None:
        time.sleep(self.delay_seconds)


class FakeEmailSender:
    def __init__(self, error: Exception | None = None):
        self.error = error
        self.records: list[dict] = []

    def send_survey(self, record: dict) -> None:
        self.records.append(record)
        if self.error:
            raise self.error


def make_settings(tmp_path: Path) -> Settings:
    return Settings(
        app_env="test",
        smtp_username="sender@example.com",
        smtp_password="secret",
        smtp_from_email="sender@example.com",
        survey_recipient_email="owner@example.com",
        survey_data_dir=tmp_path / "submissions",
        smtp_timeout_seconds=3,
        mail_send_timeout_seconds=5,
    )


def survey_payload() -> dict:
    return {
        "answers": [
            {"question": "Какой сайт нужен?", "answer": "Интернет-магазин"},
            {"question": "Какой бюджет?", "answer": "100–250 тыс. ₽"},
        ],
        "user_email": "client@example.com",
        "user_phone": "+7 999 123-45-67",
        "website": "",
    }


def test_submit_survey_sends_email_and_saves_record(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    sender = FakeEmailSender()
    store = SubmissionStore(settings.survey_data_dir)
    app = create_app(settings=settings, email_sender=sender, store=store)

    with TestClient(app) as client:
        response = client.post("/api/survey", json=survey_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "success"
    assert len(sender.records) == 1
    assert sender.records[0]["user_phone"] == "+7 999 123-45-67"

    saved_path = settings.survey_data_dir / f"{body['submission_id']}.json"
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    assert saved["email_status"] == "sent"
    assert saved["user_email"] == "client@example.com"


def test_submit_survey_returns_clear_error_and_keeps_lead(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    sender = FakeEmailSender(EmailDeliveryError("SMTP unavailable"))
    store = SubmissionStore(settings.survey_data_dir)
    app = create_app(settings=settings, email_sender=sender, store=store)

    with TestClient(app) as client:
        response = client.post("/api/survey", json=survey_payload())

    assert response.status_code == 502
    detail = response.json()["detail"]
    assert detail["code"] == "email_delivery_failed"
    saved = store.get(detail["submission_id"])
    assert saved is not None
    assert saved["email_status"] == "failed"


def test_submit_survey_validates_phone(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    app = create_app(
        settings=settings,
        email_sender=FakeEmailSender(),
        store=SubmissionStore(settings.survey_data_dir),
    )
    payload = survey_payload()
    payload["user_phone"] = "123"

    with TestClient(app) as client:
        response = client.post("/api/survey", json=payload)

    assert response.status_code == 422


def test_honeypot_does_not_send_email(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    sender = FakeEmailSender()
    app = create_app(
        settings=settings,
        email_sender=sender,
        store=SubmissionStore(settings.survey_data_dir),
    )
    payload = survey_payload()
    payload["website"] = "https://spam.example"

    with TestClient(app) as client:
        response = client.post("/api/survey", json=payload)

    assert response.status_code == 201
    assert sender.records == []


def test_health_reports_mail_configuration(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    app = create_app(
        settings=settings,
        email_sender=FakeEmailSender(),
        store=SubmissionStore(settings.survey_data_dir),
    )

    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "email_configured": True,
        "environment": "test",
    }


def test_store_lists_only_failed_submissions(tmp_path: Path) -> None:
    settings = make_settings(tmp_path)
    store = SubmissionStore(settings.survey_data_dir)

    first = store.create(SurveyData(**survey_payload()))
    second = store.create(SurveyData(**survey_payload()))
    store.update_email_status(first['id'], 'failed', 'SMTP unavailable')
    store.update_email_status(second['id'], 'sent')

    failed = store.list_by_status({'failed', 'timeout'})

    assert [record['id'] for record in failed] == [first['id']]


def test_submit_survey_stops_waiting_after_backend_timeout(tmp_path: Path) -> None:
    settings = replace(make_settings(tmp_path), mail_send_timeout_seconds=0.05)
    store = SubmissionStore(settings.survey_data_dir)
    app = create_app(
        settings=settings,
        email_sender=SlowEmailSender(delay_seconds=0.25),
        store=store,
    )

    with TestClient(app) as client:
        started_at = time.monotonic()
        response = client.post("/api/survey", json=survey_payload())
        elapsed = time.monotonic() - started_at

    assert response.status_code == 504
    assert elapsed < 1.0
    detail = response.json()["detail"]
    assert detail["code"] == "email_timeout"
    saved = store.get(detail["submission_id"])
    assert saved is not None
    assert saved["email_status"] == "timeout"
