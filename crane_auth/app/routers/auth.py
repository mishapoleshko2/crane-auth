from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from crane_auth.app.dependencies import (
    get_refresh_session_repository,
    get_refresh_token_from_cookie,
    get_user_repository,
)
from crane_auth.interactor.dto.auth import (
    UserLoginInputDTO,
    UserLogoutInputDTO,
    TokenRefreshInputDTO,
    TokenRefreshOutputDTO,
)
from crane_auth.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)
from crane_auth.interactor.ports.repositories.user import UserRepository
from crane_auth.interactor.use_cases.auth.token_refresh import TokenRefreshUseCase
from crane_auth.interactor.use_cases.auth.user_login import UserLoginUseCase
from crane_auth.interactor.use_cases.auth.user_logout import UserLogoutUseCase


auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/login", summary="user login")
async def login(
    login_data: UserLoginInputDTO,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    refresh_session_repository: Annotated[
        RefreshSessionRepository, Depends(get_refresh_session_repository)
    ],
) -> JSONResponse:
    use_case = UserLoginUseCase(user_repository, refresh_session_repository)
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
    refresh_session_repository: Annotated[
        RefreshSessionRepository, Depends(get_refresh_session_repository)
    ],
) -> Response:
    use_case = UserLogoutUseCase(refresh_session_repository)
    input_dto = UserLogoutInputDTO(refresh_token=refresh_token)
    await use_case.execute(input_dto)

    response = JSONResponse(status_code=200, content={"msg": "ok"})
    response.delete_cookie("refresh-token")
    return response


@auth_router.post("/refresh-tokens", summary="token refresh")
async def refresh_token(
    refresh_token: Annotated[UUID, Depends(get_refresh_token_from_cookie)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    refresh_session_repository: Annotated[
        RefreshSessionRepository, Depends(get_refresh_session_repository)
    ],
) -> TokenRefreshOutputDTO:
    use_case = TokenRefreshUseCase(user_repository, refresh_session_repository)
    output_dto = await use_case.execute(
        TokenRefreshInputDTO(refresh_token=refresh_token)
    )
    return output_dto
