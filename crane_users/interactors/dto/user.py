from dataclasses import dataclass


@dataclass
class CreateUserInputDTO:
    login: str
    email: str
    password: str
