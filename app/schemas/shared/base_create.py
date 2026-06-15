from pydantic import ConfigDict, BaseModel


class BaseCreate(BaseModel):
    model_config = ConfigDict(strict=True)
