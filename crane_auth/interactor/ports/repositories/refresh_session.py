from typing import Protocol

from crane_auth.domain.entities.tokens import RefreshSession
from crane_auth.domain.value_objects.types import RefreshToken


class RefreshSessionRepository(Protocol):
    async def get_session(self, token: RefreshToken) -> None | RefreshSession: ...

    async def delete_session(self, token: RefreshToken) -> None: ...

    async def create_session(self, session: RefreshSession) -> RefreshSession: ...

    async def delete_user_session(self, user_id: int) -> None: ...
