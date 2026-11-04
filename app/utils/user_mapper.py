from app.database.models.doctor import Doctor
from app.database.models.nurse import Nurse
from app.database.models.user import User
from app.schemas.doctor import DoctorRead
from app.schemas.nurse import NurseRead


def user_to_read(user: User) -> DoctorRead | NurseRead:
    if isinstance(user, Doctor):
        return DoctorRead.model_validate(user)

    if isinstance(user, Nurse):
        return NurseRead.model_validate(user)

    raise TypeError(f"Unsupported user type: {type(user).__name__}")
