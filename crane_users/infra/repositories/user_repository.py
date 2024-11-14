from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_users.domain.entities.user import User
from crane_users.interactors.ports.repositories.user import UserRepository
from crane_users.infra.sqlalchemy_db.models.user import User as DBUser


@dataclass
class PostgresUserRepository(UserRepository):
    session: AsyncSession

    async def find_user_by_email(self, email: str) -> User | None:
        query = select(DBUser).where(DBUser.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def find_user_by_login(self, login: str) -> User | None:
        query = select(DBUser).where(DBUser.login == login)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, login: str, email: str, password_hash: str) -> User:
        db_user = DBUser(login=login, email=email, password_hash=password_hash)
        self.session.add(db_user)
        await self.session.commit()
        return db_user.to_entity()

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(DBUser).where(DBUser.id == user_id))
        await self.session.commit()
