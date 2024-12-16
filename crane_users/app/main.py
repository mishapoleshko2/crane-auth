import uvicorn
import typer
from fastapi import FastAPI
from crane_users.app.routers.user import user_router
from crane_users.app.routers.auth import auth_router
from crane_users.app.error_handlers import ERROR_HANDLING_MAPPING

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)

for exc, handler in ERROR_HANDLING_MAPPING.items():
    app.add_exception_handler(exc, handler)


def main(
    host: str = typer.Argument("127.0.0.1", help="Application host"),
    port: int = typer.Argument(8000, help="Application port"),
) -> None:
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(main)
