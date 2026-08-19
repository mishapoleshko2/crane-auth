from typing import cast, Annotated
from uuid import UUID

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_auth.infra.repositories.refresh_session_repository import (
    PgRefreshSesionRepository,
)
from crane_auth.infra.repositories.user import PgUserRepository
from crane_auth.infra.sqlalchemy_db.utils import get_session
from crane_auth.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)
from crane_auth.interactor.ports.repositories.user import UserRepository

from crane_auth.app.exceptions import AutharizationError
from crane_auth.domain.value_objects.types import RefreshToken


async def get_refresh_token_from_cookie(
    request: Request,
) -> RefreshToken:
    refresh_token = request.cookies.get("refresh-token", None)
    if not refresh_token:
        raise AutharizationError("Refresh session not found")
    return cast(UUID, refresh_token)


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    repository = PgUserRepository(session)
    return repository


async def get_refresh_session_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RefreshSessionRepository:
    repository = PgRefreshSesionRepository(session)
    return repository
