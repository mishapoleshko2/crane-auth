from typing import Protocol

from crane_users.domain.entities.user import User
from crane_users.domain.value_objects.roles import UserRole


class UserRepository(Protocol):
    async def create_user(
        self, login: str, email: str, password_hash: str, role: UserRole = UserRole.user
    ) -> User: ...

    async def find_user_by_email(self, email: str) -> User | None: ...

    async def find_user_by_login(self, login: str) -> User | None: ...

    async def delete_user(self, user_id: int) -> None: ...

    async def get_user(self, user_id: int) -> User | None: ...
