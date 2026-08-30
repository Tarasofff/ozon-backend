from pydantic import BaseModel, Field, NonNegativeInt
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: NonNegativeInt
    limit: int = Field(gt=0, le=100)
    offset: NonNegativeInt = 0
