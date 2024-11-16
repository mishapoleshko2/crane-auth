from typing import NewType

import bcrypt

from pydantic import BaseModel, SecretBytes


Email = NewType("Email", str)
PSWD_CODING = "utf-8"


def hash_password(pswd: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(bytes(pswd, PSWD_CODING), salt)
    return hashed_pswd


class User(BaseModel):
    id: int
    login: str
    email: Email
    password_hash: SecretBytes
    company_id: int | None
