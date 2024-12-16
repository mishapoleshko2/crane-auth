from dataclasses import dataclass

from crane_users.domain.exceptions import RefreshSessionNotFoundException
from crane_users.interactor.dto.auth import UserLogoutInputDTO
from crane_users.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)


@dataclass
class UserLogoutUseCase:
    refresh_session_repository: RefreshSessionRepository

    async def execute(self, input_dto: UserLogoutInputDTO) -> None:
        try:
            await self.refresh_session_repository.delete_session(
                input_dto.refresh_token
            )
        except Exception:
            raise RefreshSessionNotFoundException
