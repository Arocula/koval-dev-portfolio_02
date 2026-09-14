from __future__ import annotations

from email.message import EmailMessage

import pytest

from backend.config import Settings
from backend.email_sender import EmailConfigurationError, EmailSender


class FakeSmtpSsl:
    instance: FakeSmtpSsl | None = None

    def __init__(self, host, port, timeout, context):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.context = context
        self.login_args = None
        self.sent_message: EmailMessage | None = None
        self.from_addr = None
        self.to_addrs = None
        FakeSmtpSsl.instance = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def login(self, username, password):
        self.login_args = (username, password)

    def send_message(self, message, from_addr, to_addrs):
        self.sent_message = message
        self.from_addr = from_addr
        self.to_addrs = to_addrs


def configured_settings() -> Settings:
    return Settings(
        smtp_host="smtp.example.com",
        smtp_port=465,
        smtp_security="ssl",
        smtp_auth=True,
        smtp_username="sender@example.com",
        smtp_password="abcd efgh ijkl mnop",
        smtp_from_email="sender@example.com",
        smtp_from_name="Portfolio",
        survey_recipient_email="owner@example.com",
        smtp_timeout_seconds=4,
    )


def sample_record() -> dict:
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": "2026-07-13T12:00:00+00:00",
        "user_email": "client@example.com",
        "user_phone": "+7 999 123-45-67",
        "answers": [
            {"question": "Какой сайт нужен?", "answer": "Лендинг"},
        ],
    }


def test_send_survey_uses_smtp_and_includes_contacts(monkeypatch) -> None:
    monkeypatch.setattr("backend.email_sender.smtplib.SMTP_SSL", FakeSmtpSsl)
    sender = EmailSender(configured_settings())

    sender.send_survey(sample_record())

    smtp = FakeSmtpSsl.instance
    assert smtp is not None
    assert smtp.login_args == ("sender@example.com", "abcdefghijklmnop")
    assert smtp.from_addr == "sender@example.com"
    assert smtp.to_addrs == ["owner@example.com"]
    assert smtp.sent_message is not None
    assert smtp.sent_message["Reply-To"] == "client@example.com"
    assert smtp.sent_message["X-Submission-ID"] == "123e4567-e89b-12d3-a456-426614174000"
    plain_body = smtp.sent_message.get_body(preferencelist=("plain",)).get_content()
    assert "+7 999 123-45-67" in plain_body
    assert "Какой сайт нужен?" in plain_body
    assert "Лендинг" in plain_body


def test_build_message_contains_html_and_plain_parts() -> None:
    message = EmailSender(configured_settings()).build_message(sample_record())

    assert message.is_multipart()
    assert message.get_body(preferencelist=("plain",)) is not None
    assert message.get_body(preferencelist=("html",)) is not None


def test_missing_settings_raise_clear_configuration_error() -> None:
    sender = EmailSender(Settings())

    with pytest.raises(EmailConfigurationError):
        sender.send_survey(sample_record())
