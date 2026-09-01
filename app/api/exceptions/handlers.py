from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.api.exceptions.database import map_integrity_error
from app.api.exceptions.domain import get_domain_status_code
from app.core.exceptions import DomainException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        request: Request,
        exc: DomainException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=get_domain_status_code(exc),
            content={"detail": exc.message},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request,
        exc: IntegrityError,
    ) -> JSONResponse:
        status_code, detail = map_integrity_error(exc)

        return JSONResponse(
            status_code=status_code,
            content={"detail": detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
