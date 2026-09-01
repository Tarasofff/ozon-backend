from asyncpg.exceptions import (
    CheckViolationError,
    ForeignKeyViolationError,
    NotNullViolationError,
    UniqueViolationError,
)
from fastapi import status
from sqlalchemy.exc import IntegrityError

DATABASE_ERROR_RESPONSES = {
    UniqueViolationError: (
        status.HTTP_409_CONFLICT,
        "Entity already exists",
    ),
    ForeignKeyViolationError: (
        status.HTTP_400_BAD_REQUEST,
        "Related entity does not exist",
    ),
    CheckViolationError: (
        status.HTTP_400_BAD_REQUEST,
        "Data violates database constraints",
    ),
    NotNullViolationError: (
        status.HTTP_400_BAD_REQUEST,
        "Required field is missing",
    ),
}


def map_integrity_error(exc: IntegrityError) -> tuple[int, str]:
    original = getattr(exc.orig, "__cause__", exc.orig)

    for exception_type, response in DATABASE_ERROR_RESPONSES.items():
        if isinstance(original, exception_type):
            return response

    return (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Internal server error",
    )
