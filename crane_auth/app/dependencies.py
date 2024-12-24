from typing import cast
from uuid import UUID

from fastapi import Request

from crane_auth.app.exceptions import AutharizationError
from crane_auth.domain.value_objects.types import RefreshToken


async def get_refresh_token_from_cookie(
    request: Request,
) -> RefreshToken:
    refresh_token = request.cookies.get("refresh-token", None)
    if not refresh_token:
        raise AutharizationError("Refresh session not found")
    return cast(UUID, refresh_token)
