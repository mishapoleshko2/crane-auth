from typing import TypeAlias, Any, ClassVar

from cerberus import Validator  # type: ignore

from crane_users.interactor.exceptions import DTOValidationError

Schema: TypeAlias = dict[str, dict[str, Any]]
Data: TypeAlias = dict[str, Any]


class BaseValidator:
    schema: ClassVar[Schema]

    def validate(self, data: Data) -> None:
        validator = Validator(self.schema)
        if not validator.validate(data):
            msg = self._create_error_msg(validator.errors)
            raise DTOValidationError(msg)

    def _create_error_msg(self, errors: dict[str, list[str]]) -> str:
        converted_errors = [
            f"{key.capitalize()}: {', '.join(key_errors)}"
            for key, key_errors in errors.items()
        ]
        msg = "/n".join(converted_errors)
        return msg
