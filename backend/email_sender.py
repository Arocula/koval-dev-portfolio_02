from __future__ import annotations

import html
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid
from typing import Any

from backend.config import Settings

logger = logging.getLogger(__name__)


class EmailError(RuntimeError):
    code = "email_error"
    public_message = "Не удалось отправить письмо. Попробуйте еще раз."


class EmailConfigurationError(EmailError):
    code = "email_not_configured"
    public_message = "Почта на сервере не настроена. Проверьте backend/.env."


class EmailAuthenticationError(EmailError):
    code = "email_authentication_failed"
    public_message = "Сервер не смог авторизоваться в почте. Проверьте пароль приложения."


class EmailDeliveryError(EmailError):
    code = "email_delivery_failed"
    public_message = "Почтовый сервер временно недоступен. Заявка сохранена — повторите отправку позже."


class EmailSender:
    def __init__(self, settings: Settings):
        self.settings = settings

    def send_survey(self, record: dict[str, Any]) -> None:
        if not self.settings.email_configured:
            raise EmailConfigurationError("Не заполнены обязательные SMTP-параметры")

        message = self.build_message(record)
        password = "".join(self.settings.smtp_password.split())
        context = ssl.create_default_context()

        try:
            if self.settings.smtp_security == "ssl":
                with smtplib.SMTP_SSL(
                    self.settings.smtp_host,
                    self.settings.smtp_port,
                    timeout=self.settings.smtp_timeout_seconds,
                    context=context,
                ) as server:
                    self._authenticate_and_send(server, message, password)
                return

            with smtplib.SMTP(
                self.settings.smtp_host,
                self.settings.smtp_port,
                timeout=self.settings.smtp_timeout_seconds,
            ) as server:
                server.ehlo()
                if self.settings.smtp_security == "starttls":
                    server.starttls(context=context)
                    server.ehlo()
                self._authenticate_and_send(server, message, password)

        except smtplib.SMTPAuthenticationError as exc:
            logger.exception("SMTP: ошибка авторизации")
            raise EmailAuthenticationError("SMTP authentication failed") from exc
        except (smtplib.SMTPException, TimeoutError, ConnectionError, OSError) as exc:
            logger.exception("SMTP: ошибка доставки письма")
            raise EmailDeliveryError(f"{type(exc).__name__}: {exc}") from exc

    def _authenticate_and_send(
        self,
        server: smtplib.SMTP,
        message: EmailMessage,
        password: str,
    ) -> None:
        if self.settings.smtp_auth:
            server.login(self.settings.smtp_username, password)
        server.send_message(
            message,
            from_addr=self.settings.from_email,
            to_addrs=[self.settings.recipient_email],
        )

    def build_message(self, record: dict[str, Any]) -> EmailMessage:
        answers = record.get("answers", [])
        user_email = str(record.get("user_email", ""))
        user_phone = str(record.get("user_phone", ""))
        submission_id = str(record.get("id", "без номера"))
        created_at = str(record.get("created_at", ""))

        text_lines = [
            "НОВАЯ ЗАЯВКА С САЙТА",
            "=" * 58,
            f"Номер заявки: {submission_id}",
            f"Дата (UTC): {created_at}",
            "",
            "КОНТАКТЫ",
            f"Email: {user_email}",
            f"Телефон: {user_phone}",
            "",
            "ОТВЕТЫ НА ОПРОС",
        ]
        for index, item in enumerate(answers, start=1):
            text_lines.extend(
                [
                    "",
                    f"{index}. {item.get('question', '')}",
                    f"Ответ: {item.get('answer', '')}",
                ]
            )
        text_body = "\n".join(text_lines)

        answer_rows = "".join(
            "<tr>"
            f"<td style='padding:12px;border-bottom:1px solid #dbe5ff;vertical-align:top'>{index}</td>"
            f"<td style='padding:12px;border-bottom:1px solid #dbe5ff'>{html.escape(str(item.get('question', '')))}</td>"
            f"<td style='padding:12px;border-bottom:1px solid #dbe5ff;font-weight:600'>{html.escape(str(item.get('answer', '')))}</td>"
            "</tr>"
            for index, item in enumerate(answers, start=1)
        )
        html_body = f"""
        <!doctype html>
        <html lang="ru">
          <body style="margin:0;background:#f4f7ff;font-family:Arial,sans-serif;color:#17203a">
            <div style="max-width:760px;margin:24px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 8px 28px rgba(25,75,180,.14)">
              <div style="padding:24px 28px;background:linear-gradient(135deg,#0066ff,#00aeea);color:white">
                <h1 style="margin:0;font-size:24px">Новая заявка с сайта</h1>
                <p style="margin:8px 0 0;opacity:.9">№ {html.escape(submission_id)}</p>
              </div>
              <div style="padding:24px 28px">
                <h2 style="font-size:18px;margin:0 0 12px">Контактные данные</h2>
                <p style="margin:6px 0"><strong>Email:</strong> {html.escape(user_email)}</p>
                <p style="margin:6px 0"><strong>Телефон:</strong> {html.escape(user_phone)}</p>
                <p style="margin:6px 0 22px;color:#62708f"><strong>Дата UTC:</strong> {html.escape(created_at)}</p>
                <h2 style="font-size:18px;margin:0 0 12px">Ответы на опрос</h2>
                <table role="presentation" style="width:100%;border-collapse:collapse;font-size:14px">
                  <thead>
                    <tr style="background:#eef4ff;text-align:left">
                      <th style="padding:12px">#</th>
                      <th style="padding:12px">Вопрос</th>
                      <th style="padding:12px">Ответ</th>
                    </tr>
                  </thead>
                  <tbody>{answer_rows}</tbody>
                </table>
              </div>
            </div>
          </body>
        </html>
        """

        message = EmailMessage()
        message["From"] = formataddr((self.settings.smtp_from_name, self.settings.from_email))
        message["To"] = self.settings.recipient_email
        message["Reply-To"] = user_email
        message["Subject"] = f"Новая заявка с сайта — {user_phone}"
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = make_msgid(domain=self.settings.from_email.split("@")[-1])
        message["X-Submission-ID"] = submission_id
        message.set_content(text_body)
        message.add_alternative(html_body, subtype="html")
        return message
