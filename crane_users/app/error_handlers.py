from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from crane_users.domain.exceptions import UserIsExistError
from crane_users.exceptions import SystemException
from crane_users.interactor.exceptions import DTOValidationException


__all__ = ["ERROR_HANDLING_MAPPING"]


def handle_system_exc(_: Request, exc: Exception) -> Response:
    return _handle_exception(500, str(exc))


def handle_422_exc(_: Request, exc: Exception) -> Response:
    return _handle_exception(422, str(exc))

def handle_409_exc(_: Request, exc: Exception) -> Response:
    return _handle_exception(409, str(exc))

def _handle_exception(status_code: int, msg: str) -> Response:
    return JSONResponse(status_code=status_code, content={"msg": msg})


ERROR_HANDLING_MAPPING: dict[
    type[Exception], Callable[[Request, Exception], Response]
] = {
    SystemException: handle_system_exc,
    DTOValidationException: handle_422_exc,
    UserIsExistError: handle_409_exc,
}
