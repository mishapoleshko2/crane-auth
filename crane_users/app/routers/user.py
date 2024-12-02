from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_users.interactor.use_cases.user_creating import UserCreatingUseCase
from crane_users.interactor.dto.user import UserCreatingInputDTO, UserCreatingOutputDTO
from crane_users.infra.sqlalchemy_db.utils import get_session
from crane_users.infra.repositories.user_repository import PostgresUserRepository

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserCreatingOutputDTO, summary="User creating")
async def create_user(
    creating_data: UserCreatingInputDTO,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserCreatingOutputDTO:
    user_repository = PostgresUserRepository(session)
    use_case = UserCreatingUseCase(user_repository)
    output_dto = await use_case.execute(creating_data)
    return output_dto
