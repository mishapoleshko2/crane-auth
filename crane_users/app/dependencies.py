from typing import cast, Annotated
from uuid import UUID

from fastapi import Request

from crane_users.app.exceptions import AutharizationError
from crane_users.domain.value_objects.types import RefreshToken


def get_refresh_token_from_cookie(
    request: Request,
) -> RefreshToken:
    refresh_token = request.cookies.get("refresh-token", None)
    if not refresh_token:
        raise AutharizationError
    return cast(UUID, refresh_token)
