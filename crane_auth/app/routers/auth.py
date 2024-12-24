from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_auth.app.dependencies import get_refresh_token_from_cookie
from crane_auth.infra.repositories.refresh_session_repository import (
    PgRefreshSesionRepository,
)
from crane_auth.infra.repositories.user import PgUserRepository
from crane_auth.infra.sqlalchemy_db.utils import get_session
from crane_auth.interactor.dto.auth import (
    UserLoginInputDTO,
    UserLogoutInputDTO,
    TokenRefreshInputDTO,
    TokenRefreshOutputDTO,
)
from crane_auth.interactor.use_cases.auth.token_refresh import TokenRefreshUseCase
from crane_auth.interactor.use_cases.auth.user_login import UserLoginUseCase
from crane_auth.interactor.use_cases.auth.user_logout import UserLogoutUseCase


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
async def logout(
    refresh_token: Annotated[UUID, Depends(get_refresh_token_from_cookie)],
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
) -> Response:
    refresh_session_repo = PgRefreshSesionRepository(session)
    use_case = UserLogoutUseCase(refresh_session_repo)
    input_dto = UserLogoutInputDTO(refresh_token=refresh_token)
    await use_case.execute(input_dto)

    response.delete_cookie("refresh-token")
    return response


@auth_router.post("/refresh-tokens", summary="token refresh")
async def refresh_token(
    refresh_token: Annotated[UUID, Depends(get_refresh_token_from_cookie)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TokenRefreshOutputDTO:
    refresh_session_repo = PgRefreshSesionRepository(session)
    user_repo = PgUserRepository(session)
    use_case = TokenRefreshUseCase(user_repo, refresh_session_repo)
    output_dto = await use_case.execute(
        TokenRefreshInputDTO(refresh_token=refresh_token)
    )
    return output_dto
