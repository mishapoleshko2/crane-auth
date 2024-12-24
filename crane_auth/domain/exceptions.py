from crane_auth.exceptions import SystemException


class IncorrectPasswordError(SystemException): ...


class UserIsNotRegisteredException(SystemException):
    def __init__(self) -> None:
        super().__init__("User is not registered")


class RefreshSessionNotFoundException(SystemException):
    def __init__(self) -> None:
        super().__init__("User is not authorized")


class RefreshSessionIsExpiredException(SystemException):
    def __init__(self) -> None:
        super().__init__("Refresh session timed out")


class UserIsExistError(SystemException): ...
