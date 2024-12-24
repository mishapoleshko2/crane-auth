from typing import cast

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM
from pydantic import SecretStr

from crane_auth.domain.entities.user import User as DomainUser, Email
from crane_auth.infra.sqlalchemy_db.base import Base
from crane_auth.domain.value_objects.roles import UserRole


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        ENUM(UserRole, name="user_role_enum", create_type=False), nullable=False
    )

    def to_entity(self) -> DomainUser:
        return DomainUser(
            id=self.id,
            login=self.login,
            email=cast(Email, self.email),
            password_hash=cast(SecretStr, self.password_hash),
            company_id=None,
            role=self.role,
        )
