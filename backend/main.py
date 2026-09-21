from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.config import Settings, get_settings
from backend.email_sender import EmailError, EmailSender
from backend.schemas import HealthResponse, SurveyData, SurveySubmissionResponse
from backend.storage import SubmissionStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(
    settings: Settings | None = None,
    email_sender: EmailSender | None = None,
    store: SubmissionStore | None = None,
) -> FastAPI:
    app_settings = settings or get_settings()
    app_email_sender = email_sender or EmailSender(app_settings)
    app_store = store or SubmissionStore(app_settings.survey_data_dir)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        logger.info(
            "Backend запущен. SMTP настроен: %s",
            "да" if app_settings.email_configured else "нет",
        )
        yield

    application = FastAPI(
        title=app_settings.app_name,
        version="2.0.0",
        description="API портфолио и отправки результатов опроса",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(app_settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Accept"],
    )

    application.state.settings = app_settings
    application.state.email_sender = app_email_sender
    application.state.submission_store = app_store

    @application.get("/", tags=["system"])
    async def read_root() -> dict[str, str]:
        return {"message": "FastAPI Backend работает!"}

    @application.get("/api/hello", tags=["system"])
    async def api_hello() -> dict[str, str | int]:
        return {
            "message": "Привет от FastAPI!",
            "tech": "React + FastAPI",
            "year": 2026,
        }

    @application.get("/api/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        return HealthResponse(
            email_configured=app_settings.email_configured,
            environment=app_settings.app_env,
        )

    @application.post(
        "/api/survey",
        response_model=SurveySubmissionResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["survey"],
    )
    async def submit_survey(data: SurveyData) -> SurveySubmissionResponse:
        """Сохраняет заявку и отправляет ее на почту с ограничением времени ожидания."""

        # Honeypot: обычный пользователь это поле не видит и не заполняет.
        if data.website:
            logger.info("Отклонена вероятная бот-заявка")
            return SurveySubmissionResponse(
                message="Заявка отправлена",
                submission_id=str(uuid4()),
            )

        try:
            record = app_store.create(data)
        except OSError as exc:
            logger.exception("Не удалось сохранить заявку")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "submission_storage_failed",
                    "message": "Не удалось сохранить заявку. Проверьте права на папку backend/data.",
                },
            ) from exc

        submission_id = str(record["id"])
        try:
            await asyncio.wait_for(
                asyncio.to_thread(app_email_sender.send_survey, record),
                timeout=app_settings.mail_send_timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            app_store.update_email_status(submission_id, "timeout", "SMTP timeout")
            logger.error("Таймаут отправки заявки %s", submission_id)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail={
                    "code": "email_timeout",
                    "message": "Почтовый сервер не ответил вовремя. Заявка сохранена; повторите отправку позже.",
                    "submission_id": submission_id,
                },
            ) from exc
        except EmailError as exc:
            app_store.update_email_status(submission_id, "failed", str(exc))
            logger.error("Не отправлена заявка %s: %s", submission_id, exc)
            http_status = (
                status.HTTP_503_SERVICE_UNAVAILABLE
                if exc.code == "email_not_configured"
                else status.HTTP_502_BAD_GATEWAY
            )
            raise HTTPException(
                status_code=http_status,
                detail={
                    "code": exc.code,
                    "message": exc.public_message,
                    "submission_id": submission_id,
                },
            ) from exc
        except Exception as exc:
            app_store.update_email_status(submission_id, "failed", type(exc).__name__)
            logger.exception("Непредвиденная ошибка отправки заявки %s", submission_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "unexpected_email_error",
                    "message": "Произошла внутренняя ошибка. Заявка сохранена.",
                    "submission_id": submission_id,
                },
            ) from exc

        app_store.update_email_status(submission_id, "sent")
        logger.info("Заявка %s успешно отправлена", submission_id)
        return SurveySubmissionResponse(
            message="Результаты опроса отправлены",
            submission_id=submission_id,
        )

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
