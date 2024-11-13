from typing import Protocol

from crane_users.domain.entities.user import User


class UserRepository(Protocol):
    async def create_user(self, login: str, email: str, password_hash: str) -> User: ...

    async def find_user_by_email(self, email: str) -> User | None: ...

    async def find_user_by_login(self, login: str) -> User | None: ...

    async def delete_user(self, user_id: int) -> None: ...
