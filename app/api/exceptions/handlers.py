from asyncpg.exceptions import (
    CheckViolationError,
    ForeignKeyViolationError,
    NotNullViolationError,
    UniqueViolationError,
)
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


from app.core.exceptions import (
    AccessDeniedException,
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidCredentialsException,
)


def _get_db_error(exc: IntegrityError) -> tuple[int, str]:
    original = getattr(exc.orig, "__cause__", exc.orig)

    if isinstance(original, UniqueViolationError):
        return status.HTTP_409_CONFLICT, "Entity already exists"

    if isinstance(original, ForeignKeyViolationError):
        return status.HTTP_400_BAD_REQUEST, "Related entity does not exist"

    if isinstance(original, CheckViolationError):
        return (
            status.HTTP_400_BAD_REQUEST,
            "Data violates database constraints",
        )

    if isinstance(original, NotNullViolationError):
        return status.HTTP_400_BAD_REQUEST, "Required field is missing"

    return status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(
        request: Request,
        exc: EntityNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(EntityAlreadyExistsException)
    async def entity_already_exists_handler(
        request: Request,
        exc: EntityAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(AccessDeniedException)
    async def access_denied_handler(
        request: Request,
        exc: AccessDeniedException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        request: Request,
        exc: DomainException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request,
        exc: IntegrityError,
    ) -> JSONResponse:
        status_code, detail = _get_db_error(exc)
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
