from dataclasses import dataclass


from crane_users.interactor.dto.user import UserCreatingInputDTO
from crane_users.interactor.ports.repositories.user import UserRepository


@dataclass
class UserCreatingUseCase:
    user_repository: UserRepository

    async def execute(self, input_dto: UserCreatingInputDTO) -> None:
        pass
