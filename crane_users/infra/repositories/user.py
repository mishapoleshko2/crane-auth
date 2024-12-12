from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_users.domain.entities.user import User
from crane_users.domain.value_objects.roles import UserRole
from crane_users.interactor.ports.repositories.user import UserRepository
from crane_users.infra.sqlalchemy_db.models.user import User as DBUser


@dataclass
class PgUserRepository(UserRepository):
    session: AsyncSession

    async def find_user_by_email(self, email: str) -> User | None:
        query = select(DBUser).where(DBUser.email == email)
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        user = db_user.to_entity() if db_user else None
        return user

    async def find_user_by_login(self, login: str) -> User | None:
        query = select(DBUser).where(DBUser.login == login)
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        user = db_user.to_entity() if db_user else None
        return user

    async def create_user(
        self, login: str, email: str, password_hash: str, role: UserRole = UserRole.user
    ) -> User:
        db_user = DBUser(
            login=login, email=email, password_hash=password_hash, role=role
        )
        self.session.add(db_user)
        await self.session.commit()
        return db_user.to_entity()

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(DBUser).where(DBUser.id == user_id))
        await self.session.commit()
