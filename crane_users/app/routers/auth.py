from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_users.infra.repositories.refresh_session_repository import (
    PgRefreshSesionRepository,
)
from crane_users.infra.repositories.user import PgUserRepository
from crane_users.infra.sqlalchemy_db.utils import get_session
from crane_users.interactor.dto.auth import UserLoginInputDTO
from crane_users.interactor.use_cases.auth.user_login import UserLoginUseCase


auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/login", summary="user login")
async def login(
    login_data: UserLoginInputDTO,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> JSONResponse:
    user_repo = PgUserRepository(session)
    refresh_session_repo = PgRefreshSesionRepository(session)
    use_case = UserLoginUseCase(user_repo, refresh_session_repo)
    output_dto = await use_case.execute(login_data)

    response = JSONResponse(
        content={
            "access_token": output_dto.access_token,
        }
    )
    response.set_cookie(
        key="refresh-token",
        value=str(output_dto.refresh_token),
        httponly=True,
        max_age=output_dto.refresh_token_ttl,
        expires=output_dto.refresh_token_expires,
    )
    return response


@auth_router.post("/logout", summary="user logout")
async def logout():
    pass


@auth_router.post("refresh-tokens", summary="token refresh")
async def refresh_token():
    pass
