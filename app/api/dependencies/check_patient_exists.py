from fastapi import Depends
from app.api.exceptions.api_exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)
from app.db.session import get_session
from app.repository import PatientRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.patient import PatientCreate


def get_patient_repo(
    session: AsyncSession = Depends(get_session),
) -> PatientRepository:
    return PatientRepository(session=session)


async def check_patient_exists_by_id(
    patient_id: int, patient_repo: PatientRepository = Depends(get_patient_repo)
) -> int:
    result = await patient_repo.get_by_id(patient_id)
    if not result:
        raise NotFoundException(f"Patient id:{patient_id} not found")
    return patient_id


async def check_patient_exists_by_phone(
    patient_data: PatientCreate,
    patient_repo: PatientRepository = Depends(get_patient_repo),
):
    phone = patient_data.model_dump()["phone"]
    result = await patient_repo.get_by_phone(phone)
    if result:
        raise UnprocessableEntityException(f"Patient {phone} already exists")

    return patient_data
