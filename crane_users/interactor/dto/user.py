from typing import Any

from dataclasses import dataclass, asdict


@dataclass
class UserCreatingInputDTO:
    login: str
    email: str
    password: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UserCreatingOutputDTO(UserCreatingInputDTO):
    id: int
