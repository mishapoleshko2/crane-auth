from uuid import UUID
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from crane_users.infra.sqlalchemy_db.base import Base
from crane_users.domain.entities.tokens import RefreshSession as DomainRefreshSession


class RefreshSession(Base):
    __tablename__ = "refresh_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    ttl: Mapped[int] = mapped_column(nullable=False)
    created_dt: Mapped[datetime] = mapped_column(nullable=False)

    def to_entity(self) -> DomainRefreshSession:
        return DomainRefreshSession(
            user_id=self.user_id,
            token=self.token,
            ttl=self.ttl,
            created_dt=self.created_dt,
        )
