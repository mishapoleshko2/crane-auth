from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from crane_users.exceptions import SystemException
from crane_users.interactor.exceptions import DTOValidationException


__all__ = ["ERROR_HANDLING_MAPPING"]


def handle_system_exc(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=500, content={"msg": str(exc)})


def handle_dto_validation_exc(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=422, content={"msg": str(exc)})


ERROR_HANDLING_MAPPING: dict[
    type[Exception], Callable[[Request, Exception], Response]
] = {
    SystemException: handle_system_exc,
    DTOValidationException: handle_dto_validation_exc,
}
