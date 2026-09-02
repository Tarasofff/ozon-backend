from typing import Any, Dict
from pydantic import ConfigDict, model_validator
from app.infrastructure.security.hash import hash_password_str


class PasswordHashMixin: # TODO
    model_config = ConfigDict(strict=True)

    @model_validator(mode="before")
    @classmethod
    def hash_password(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        pwd = values.get("password")
        if pwd is None:
            return values

        values["password"] = hash_password_str(pwd)
        return values
