from typing import TypedDict, Any, cast
from uuid import uuid4
from datetime import datetime, timedelta, UTC

import jwt
from pydantic import BaseModel, Field

from crane_users.settings import settings
from crane_users.domain.value_objects.types import RefreshToken, JWTToken
from crane_users.domain.entities.user import User


class RefreshSession(BaseModel):
    user_id: int
    token: RefreshToken = Field(default_factory=uuid4)
    ttl: int = Field(default=settings.refresh_token_ttl)
    created_dt: datetime = Field(default=datetime.now())

    @property
    def expire_time(self) -> datetime:
        dt = self.created_dt + timedelta(seconds=self.ttl)
        return dt

    def is_fresh(self, when: datetime = datetime.now(UTC)) -> bool:
        return when - self.created_dt <= timedelta(seconds=self.ttl)


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


def generate_user_access_token(user: User, now: datetime) -> JWTToken:
    access_token = generate_access_token(
        {
            "user_id": user.id,
            "company_id": user.company_id,
            "exp": calc_access_token_expiration(now),
        }
    )
    return access_token
