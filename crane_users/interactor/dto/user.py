from dataclasses import dataclass


@dataclass
class UserCreatingInputDTO:
    login: str
    email: str
    password: str
