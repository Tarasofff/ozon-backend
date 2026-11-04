from typing import Annotated
from pydantic import Field

FirstNameStr = Annotated[str, Field(min_length=2, max_length=50)]
LastNameStr = Annotated[str, Field(min_length=2, max_length=50)]
PatronymicStr = Annotated[str | None, Field(min_length=2, max_length=50)]
PhoneStr = Annotated[str, Field(min_length=5, max_length=15)]
