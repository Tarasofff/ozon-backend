from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AccessDeniedException,
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidCredentialsException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(EntityAlreadyExistsException)
    async def entity_exists_handler(
        request: Request, exc: EntityAlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request, exc: InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(AccessDeniedException)
    async def access_denied_handler(request: Request, exc: AccessDeniedException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
