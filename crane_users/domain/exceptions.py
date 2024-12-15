from crane_users.exceptions import SystemException


class IncorrectPasswordError(SystemException):
    def __init__(self) -> None:
        super().__init__("Invalid password")


class UserNotFoundError(SystemException):
    def __init__(self) -> None:
        super().__init__("User not found")


class RefreshSessionNotFoundException(SystemException): ...
