from database.models.doctor import Doctor
from database.models.nurse import Nurse
from database.models.user import User
from schemas.doctor import DoctorRead
from schemas.nurse import NurseRead


def user_to_read(user: User) -> DoctorRead | NurseRead:
    if isinstance(user, Doctor):
        return DoctorRead.model_validate(user)

    if isinstance(user, Nurse):
        return NurseRead.model_validate(user)

    raise TypeError(f"Unsupported user type: {type(user).__name__}")
