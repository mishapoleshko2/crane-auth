from typing import TypeAlias, Any, ClassVar

from cerberus import Validator

Schema: TypeAlias = dict[str, dict[str, Any]]
Data: TypeAlias = dict[str, Any]


class ValidationError(ValueError): ...


class BaseValidator:
    shcema: ClassVar[Schema]

    def validate(self, data: Data) -> None:
        validator = Validator(self.shcema)
        if not validator.validate(data):
            msg = self._create_error_msg(validator.errors)
            raise ValidationError(msg)

    def _create_error_msg(errors: dict[str, list[str]]) -> str:
        errors = [
            f"{key.capitalize()}: {', '.join(key_errors)}"
            for key, key_errors in errors.items()
        ]
        msg = "/n".join(errors)
        return msg
