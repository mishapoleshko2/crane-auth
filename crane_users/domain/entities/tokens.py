from typing import TypedDict, Any, cast
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timedelta

import jwt

from crane_users.settings import settings
from crane_users.domain.value_objects.types import RefreshToken, JWTToken


class RefreshSession(BaseModel):
    user_id: int
    token: RefreshToken = Field(default_factory=uuid4)
    ttl: int = Field(default=settings.refresh_token_ttl)
    created_dt: datetime = Field(default=datetime.now())

    @property
    def expire_time(self) -> datetime:
        dt = self.created_dt + timedelta(seconds=self.ttl)
        return dt


class JWTPayload(TypedDict):
    user_id: int
    company_id: int | None
    exp: datetime


def generate_access_token(payload: JWTPayload) -> JWTToken:
    pld = cast(dict[str, Any], payload)
    token = jwt.encode(pld, settings.jwt_secret, settings.jwt_encoding_algorithm)
    return token


def calc_access_token_expiration(created_dt: datetime) -> datetime:
    expiration = created_dt + timedelta(seconds=settings.access_token_ttl)
    return expiration
