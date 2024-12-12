from crane_users.exceptions import SystemException


class DTOValidationException(SystemException):
    def __init__(self, validation_msg: str) -> None:
        super().__init__(f"Invalid data: {validation_msg}")
