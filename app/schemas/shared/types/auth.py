from typing import Annotated
from pydantic import Field

PasswordStr = Annotated[str, Field(min_length=4, max_length=255)]
