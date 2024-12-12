from typing import NewType

import bcrypt

from pydantic import SecretStr, BaseModel

from crane_users.domain.value_objects.roles import UserRole


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
    role: UserRole

    def is_me(self, password: str) -> bool:
        # TODO (poleshkomi): Understand type conversion
        ans = bcrypt.checkpw(
            bytes(password, PSWD_CODING), bytes(str(self.password_hash), PSWD_CODING)
        )
        return ans
