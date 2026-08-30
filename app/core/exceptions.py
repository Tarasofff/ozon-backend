class DomainException(Exception):
    """Базовое исключение для бизнес-логики."""

    def __init__(self, message: str = "Business logic error"):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    def __init__(self, message: str = "Entity not found"):
        super().__init__(message)


class EntityAlreadyExistsException(DomainException):
    def __init__(self, message: str = "Entity already exists"):
        super().__init__(message)


class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)


class AccessDeniedException(DomainException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message)
