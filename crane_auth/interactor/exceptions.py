from crane_auth.exceptions import SystemException


class IncorrectPasswordError(SystemException):
    def __init__(self) -> None:
        super().__init__("Incorrect login/email or password")


class UserIsNotRegisteredException(SystemException):
    def __init__(self) -> None:
        super().__init__("User is not registered")


class RefreshSessionNotFoundException(SystemException):
    def __init__(self) -> None:
        super().__init__("User is not authorized")


class RefreshSessionIsExpiredException(SystemException):
    def __init__(self) -> None:
        super().__init__("Refresh session timed out")


class UserIsExistError(SystemException):
    def __init__(self) -> None:
        super().__init__("User with the same login/email is exist")

class DTOValidationException(SystemException):
	def __init__(self, validation_msg: str) -> None:
		super().__init__(f"Invalid data: {validation_msg}")