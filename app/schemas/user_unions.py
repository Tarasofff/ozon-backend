from typing import Annotated

from pydantic import Field
from app.schemas.doctor import DoctorCreate, DoctorRead
from app.schemas.nurse import NurseCreate, NurseRead

UserCreateUnion = Annotated[DoctorCreate | NurseCreate, Field(discriminator="role")]

UserReadUnion = Annotated[DoctorRead | NurseRead, Field(discriminator="role")]
