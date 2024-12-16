from typing import Any
from datetime import datetime

from pydantic import BaseModel

from crane_users.domain.value_objects.types import RefreshToken, JWTToken


class UserLoginInputDTO(BaseModel):
    login: str | None = None
    email: str | None = None
    password: str

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump()


class UserLoginOutputDTO(BaseModel):
    access_token: JWTToken
    refresh_token: RefreshToken
    refresh_token_ttl: int
    refresh_token_expires: datetime


class UserLogoutInputDTO(BaseModel):
    refresh_token: RefreshToken


TokenRefreshInputDTO = UserLogoutInputDTO


class TokenRefreshOutputDTO(BaseModel):
    access_token: JWTToken
