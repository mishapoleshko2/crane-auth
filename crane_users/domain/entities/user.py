from typing import NewType

from pydantic import BaseModel, SecretStr


Email = NewType("Email", str)


class User(BaseModel):
    id: int
    login: str
    email: Email
    password: SecretStr
    company_id: int | None
