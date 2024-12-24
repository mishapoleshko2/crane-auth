from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from crane_auth.infra.sqlalchemy_db.base import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
