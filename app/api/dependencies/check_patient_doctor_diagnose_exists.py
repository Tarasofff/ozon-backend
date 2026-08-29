from fastapi import Depends
from app.api.exceptions.api_exceptions import NotFoundException
from app.database.session import get_session
from app.repository import PatientDoctorDiagnoseRepository
from sqlalchemy.ext.asyncio import AsyncSession


def get_treatment_plan_repo(
    session: AsyncSession = Depends(get_session),
) -> PatientDoctorDiagnoseRepository:
    return PatientDoctorDiagnoseRepository(session=session)


async def check_treatment_plan_exists(
    treatment_plan_id: int,
    treatment_plan_repo: PatientDoctorDiagnoseRepository = Depends(
        get_treatment_plan_repo
    ),
) -> int:
    result = await treatment_plan_repo.get_by_id(treatment_plan_id)
    if not result:
        raise NotFoundException(
            f"Patient_doctor_diagnose id:{treatment_plan_id} not found"
        )
    return treatment_plan_id
