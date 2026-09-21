from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class SurveyAnswer(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=2, max_length=500)
    answer: str = Field(min_length=1, max_length=500)


class SurveyData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    answers: list[SurveyAnswer] = Field(min_length=1, max_length=30)
    user_email: EmailStr
    user_phone: str = Field(min_length=7, max_length=40)
    website: str = Field(default="", max_length=200, description="Антиспам-поле")

    @field_validator("user_phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"[0-9+()\-\s.]+", value):
            raise ValueError("Телефон содержит недопустимые символы")
        digits = re.sub(r"\D", "", value)
        if not 7 <= len(digits) <= 15:
            raise ValueError("Введите корректный номер телефона")
        return value


class SurveySubmissionResponse(BaseModel):
    status: Literal["success"] = "success"
    message: str
    submission_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    email_configured: bool
    environment: str
