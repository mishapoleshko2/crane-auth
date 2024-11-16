from dataclasses import dataclass


from crane_users.interactor.dto.user import UserCreatingInputDTO
from crane_users.interactor.ports.repositories.user import UserRepository
from crane_users.interactor.validations.creating_user import CreatingUserDataValidation
from crane_users.domain.entities.user import hash_password, User


@dataclass
class UserCreatingUseCase:
    user_repository: UserRepository

    async def execute(self, input_dto: UserCreatingInputDTO) -> User:
        validation = CreatingUserDataValidation()
        validation.validate(input_dto.as_dict())

        hashed_pswd = hash_password(input_dto.password)
        user = await self.user_repository.create_user(
            input_dto.login, input_dto.email, hashed_pswd
        )

        return user
