from dataclasses import dataclass


from crane_auth.interactor.dto.user import UserCreatingInputDTO, UserCreatingOutputDTO
from crane_auth.interactor.ports.repositories.user import UserRepository
from crane_auth.interactor.validations.user_creating import UserCreatingDataValidator
from crane_auth.domain.entities.user import hash_password


@dataclass
class UserCreatingUseCase:
    user_repository: UserRepository

    async def execute(self, input_dto: UserCreatingInputDTO) -> UserCreatingOutputDTO:
        validation = UserCreatingDataValidator()
        validation.validate(input_dto.as_dict())

        hashed_pswd = hash_password(input_dto.password)
        user = await self.user_repository.create_user(
            input_dto.login, input_dto.email, hashed_pswd
        )

        output_dto = UserCreatingOutputDTO(
            id=user.id,
            login=user.login,
            email=user.email,
            password=input_dto.password,
        )

        return output_dto
