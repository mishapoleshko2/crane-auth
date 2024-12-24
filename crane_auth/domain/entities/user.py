from typing import NewType

import bcrypt

from pydantic import SecretStr, BaseModel

from crane_auth.domain.value_objects.roles import UserRole


Email = NewType("Email", str)
PSWD_CODING = "utf-8"


def hash_password(pswd: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(bytes(pswd, PSWD_CODING), salt)
    return hashed_pswd.decode(PSWD_CODING)


class User(BaseModel):
    id: int
    login: str
    email: Email
    password_hash: SecretStr
    company_id: int | None
    role: UserRole

    def is_me(self, password: str) -> bool:
        b_password = bytes(password, PSWD_CODING)
        b_password_hash = bytes(self.password_hash.get_secret_value(), PSWD_CODING)
        ans = bcrypt.checkpw(b_password, b_password_hash)
        return ans
