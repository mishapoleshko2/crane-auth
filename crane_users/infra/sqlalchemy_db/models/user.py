from typing import cast

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import SecretStr

from crane_users.domain.entities.user import User as DomainUser, Email
from crane_users.infra.sqlalchemy_db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    def to_entity(self) -> DomainUser:
        return DomainUser(
            id=self.id,
            login=self.login,
            email=cast(Email, self.email),
            password_hash=cast(SecretStr, self.password_hash),
            company_id=None,
        )
