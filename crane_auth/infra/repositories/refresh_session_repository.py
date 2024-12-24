from dataclasses import dataclass

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete

from crane_auth.domain.entities.tokens import RefreshSession
from crane_auth.interactor.ports.repositories.refresh_session import (
    RefreshSessionRepository,
)
from crane_auth.infra.sqlalchemy_db.models.refres_session import (
    RefreshSession as DBRefreshSession,
)
from crane_auth.domain.value_objects.types import RefreshToken


@dataclass
class PgRefreshSesionRepository(RefreshSessionRepository):
    session: AsyncSession

    async def get_session(self, token: RefreshToken) -> None | RefreshSession:
        query = select(DBRefreshSession).where(DBRefreshSession.token == token)
        result = await self.session.execute(query)
        db_session = result.scalar_one_or_none()
        session = db_session.to_entity() if db_session else None
        return session

    async def delete_user_session(self, user_id: int) -> None:
        query = delete(DBRefreshSession).where(DBRefreshSession.user_id == user_id)
        await self.session.execute(query)
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

    async def delete_session(self, token: RefreshToken) -> None:
        query = delete(DBRefreshSession).where(DBRefreshSession.token == token)
        await self.session.execute(query)
        await self.session.commit()
