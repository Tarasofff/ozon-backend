from pydantic import ConfigDict
from .base_entity import BaseEntity


class BaseRead(BaseEntity):
    model_config = ConfigDict(from_attributes=True)