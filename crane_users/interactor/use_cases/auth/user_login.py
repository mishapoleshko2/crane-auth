from dataclasses import dataclass
from typing import cast
from datetime import datetime, UTC

from crane_users.domain.entities.tokens import (
    RefreshSession,
    calc_access_token_expiration,
    generate_access_token,
)
from crane_users.domain.exceptions import UserNotFoundError, IncorrectPasswordError
from crane_users.interactor.dto.auth import UserLoginInputDTO, UserLoginOutputDTO
from crane_users.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)
from crane_users.interactor.ports.repositories.user import UserRepository
from crane_users.interactor.validations.user_creating import UserCreatingDataValidator


@dataclass
class UserLoginUseCase:
    user_repository: UserRepository
    refresh_session_repository: RefreshSessionRepository

    async def execute(self, input_dto: UserLoginInputDTO) -> UserLoginOutputDTO:
        validator = UserCreatingDataValidator()
        validator.validate(input_dto.as_dict())

        if input_dto.email:
            user = await self.user_repository.find_user_by_email(input_dto.email)
        else:
            user = await self.user_repository.find_user_by_login(
                cast(str, input_dto.login)
            )

        if not user:
            raise UserNotFoundError

        if not user.is_me(input_dto.password):
            raise IncorrectPasswordError

        now = datetime.now(UTC)
        refresh_session = RefreshSession(user_id=user.id, created_dt=now)
        await self.refresh_session_repository.create_session(refresh_session)

        access_token = generate_access_token(
            {
                "user_id": user.id,
                "company_id": user.company_id,
                "exp": calc_access_token_expiration(now),
            }
        )

        return UserLoginOutputDTO(
            access_token=access_token,
            refresh_token=refresh_session.token,
            refresh_token_ttl=refresh_session.ttl,
            refresh_token_expires=refresh_session.expire_time,
        )
