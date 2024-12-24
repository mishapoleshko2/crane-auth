from typing import Any

from pydantic import BaseModel


class UserCreatingInputDTO(BaseModel):
    login: str
    email: str
    password: str

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump()


class UserCreatingOutputDTO(UserCreatingInputDTO):
    id: int
