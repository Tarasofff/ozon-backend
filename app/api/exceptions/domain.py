from fastapi import status

from app.core.exceptions import (
    AccessDeniedException,
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidCredentialsException,
)

DOMAIN_EXCEPTION_STATUS = {
    EntityNotFoundException: status.HTTP_404_NOT_FOUND,
    EntityAlreadyExistsException: status.HTTP_409_CONFLICT,
    InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
    AccessDeniedException: status.HTTP_403_FORBIDDEN,
}


def get_domain_status_code(exc: DomainException) -> int:
    for exception_type, status_code in DOMAIN_EXCEPTION_STATUS.items():
        if isinstance(exc, exception_type):
            return status_code

    return status.HTTP_400_BAD_REQUEST
