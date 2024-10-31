from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from crane_users.infra.sqlalchemy_db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
