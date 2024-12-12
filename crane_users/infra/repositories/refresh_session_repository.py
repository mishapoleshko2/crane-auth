from dataclasses import dataclass

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from crane_users.domain.entities.tokens import RefreshSession
from crane_users.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)
from crane_users.infra.sqlalchemy_db.models.refres_session import (
    RefreshSession as DBRefreshSession,
)
from crane_users.domain.value_objects.types import RefreshToken


@dataclass
class PgRefreshSesionRepository(RefreshSessionRepository):
    session: AsyncSession

    async def get_session(self, token: RefreshToken) -> None | RefreshSession:
        query = select(DBRefreshSession).where(DBRefreshSession.token == token)
        result = await self.session.execute(query)
        db_session = result.scalar_one_or_none()
        session = db_session.to_entity() if db_session else None
        return session

    async def delete_session(self, token: RefreshToken) -> None:
        r_session = self.get_session(token)
        if not r_session:
            raise

        await self.session.delete(r_session)
        await self.session.commit()

    async def create_session(self, session: RefreshSession) -> RefreshSession:
        db_session = DBRefreshSession(
            token=session.token,
            user_id=session.user_id,
            ttl=session.ttl,
            created_dt=session.created_dt,
        )
        self.session.add(db_session)
        await self.session.commit()
        return session
