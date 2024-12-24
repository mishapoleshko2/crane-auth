from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from crane_auth.domain.exceptions import UserIsExistError
from crane_auth.domain.entities.user import User
from crane_auth.domain.value_objects.roles import UserRole
from crane_auth.interactor.ports.repositories.user import UserRepository
from crane_auth.infra.sqlalchemy_db.models.user import User as DBUser


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
        try:
            await self.session.commit()
        except Exception as e:
            if isinstance(e, IntegrityError) and "duplicate key value" in str(e):
                raise UserIsExistError(
                    "User with the same login/email is exist"
                ) from None
            raise e
        return db_user.to_entity()

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(DBUser).where(DBUser.id == user_id))
        await self.session.commit()

    async def get_user(self, user_id: int) -> User | None:
        db_user = await self.session.get(DBUser, user_id)
        user = db_user.to_entity() if db_user else None
        return user
