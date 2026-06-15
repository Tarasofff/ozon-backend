from pydantic import BaseModel


class TokenSchema(BaseModel):
    token: str
    token_type: str
