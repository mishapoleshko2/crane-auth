class SystemException(Exception): ...


class DTOValidationError(Exception):
    def __init__(self, validation_msg: str) -> None:
        super().__init__(f"Invalid data: {validation_msg}")
