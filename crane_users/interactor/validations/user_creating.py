from typing import Callable
import re

from crane_users.interactor.validations.base import BaseValidator


def validate_password(
    field: str, value: str, error: Callable[[str, str], None]
) -> None:
    if re.search("[0-9]", value) is None:
        error(field, "not contain at least one number")
    if len(value) < 8 or len(value) > 20:
        error(field, "length should be between 8 and 20 symbols")


def validate_email(field: str, value: str, error: Callable[[str, str], None]) -> None:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        error(field, "invalid value")


class UserCreatingDataValidator(BaseValidator):
    schema = {
        "login": {"type": "string", "required": True},
        "email": {"type": "string", "required": True, "check_with": validate_email},
        "password": {
            "type": "string",
            "required": True,
            "check_with": validate_password,
        },
    }
