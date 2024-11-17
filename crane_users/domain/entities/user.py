from typing import NewType

import bcrypt

from pydantic import BaseModel, SecretStr


Email = NewType("Email", str)
PSWD_CODING = "utf-8"


def hash_password(pswd: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(bytes(pswd, PSWD_CODING), salt)
    return str(hashed_pswd)


class User(BaseModel):
    id: int
    login: str
    email: Email
    password_hash: SecretStr
    company_id: int | None
