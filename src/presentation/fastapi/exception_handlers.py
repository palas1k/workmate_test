from collections.abc import Awaitable
from collections.abc import Callable
from typing import TypeVar

import orjson

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.errors import BaseError
from src.application.errors import BaseErrorGroup
from src.application.errors import DatabaseError
from src.application.errors import NotFoundError

TError = TypeVar('TError', bound=BaseError)


def _make_exception_handler(
        ex_type: type[TError],
) -> Callable[[Request, TError], Awaitable[JSONResponse]]:
    async def exception_handler(request: Request, exc: TError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={'errors': [str(exc)]},
        )

    return exception_handler


async def _exception_group_handler(
        request: Request, exc: BaseErrorGroup
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'errors': [str(exc) for exc in exc.exceptions]},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Установка обработчиков ошибок FastAPI."""
    for exc_type in [
        BaseError,
        DatabaseError,
        NotFoundError,
    ]:
        app.exception_handler(exc_type)(_make_exception_handler(exc_type))
    app.exception_handler(BaseErrorGroup)(_exception_group_handler)
