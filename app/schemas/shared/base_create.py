from pydantic import ConfigDict
from app.schemas.shared.base_schema import BaseSchema


class BaseCreate(BaseSchema):
    model_config = ConfigDict(strict=True, extra="forbid")  # TODO test
