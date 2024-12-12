from typing import Protocol

from crane_users.domain.entities.tokens import RefreshSession
from crane_users.domain.value_objects.types import RefreshToken


class RefreshSessionRepository(Protocol):
    async def get_session(self, token: RefreshToken) -> None | RefreshSession: ...

    async def delete_session(self, token: RefreshToken) -> None: ...

    async def create_session(self, session: RefreshSession) -> RefreshSession: ...
