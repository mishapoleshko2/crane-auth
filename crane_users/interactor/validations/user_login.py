from cerberus import Validator  # type: ignore

from crane_users.interactor.validations.base import BaseValidator


class ValidatorEngine(Validator):
    def _validate_is_login_or_email_set(
        self, login_or_email_set: bool, field: str, value: str | None
    ) -> None:
        "{'type': 'boolean'}"
        if not login_or_email_set:
            return
        email = self.document.get("email")
        if not email and not value:
            self._error(field, "email or login are required")


class UserLoginDataValidator(BaseValidator):
    validator_engine = ValidatorEngine
    schema = {
        "password": {"type": "string", "required": True},
        "email": {"type": "string", "required": True, "nullable": True},
        "login": {"is_login_or_email_set": True, "type": "string", "nullable": True},
    }
