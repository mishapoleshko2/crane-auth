from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends

from crane_auth.app.dependencies import get_user_repository
from crane_auth.interactor.ports.repositories.user import UserRepository
from crane_auth.interactor.use_cases.user_creating import UserCreatingUseCase
from crane_auth.interactor.dto.user import UserCreatingInputDTO, UserCreatingOutputDTO

user_router = APIRouter(prefix="/api/auth/users", tags=["Users"])


@user_router.post("/", response_model=UserCreatingOutputDTO, summary="User creating")
async def create_user(
    creating_data: UserCreatingInputDTO,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserCreatingOutputDTO:
    use_case = UserCreatingUseCase(user_repository)
    output_dto = await use_case.execute(creating_data)
    return output_dto
