from fastapi import APIRouter, Depends, Query, status
from app.api.dependencies import check_token
from app.config.config import app_config
from app.db.session import get_session
from app.repository import DoctorRepository, SpecializationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.doctor import PaginatedDoctorsResponse
from app.schemas.specialization import PaginatedDoctorSpecializationsResponse

router = APIRouter(
    prefix=app_config.api_v1_prefix.doctor,
    tags=["Doctors"],
    dependencies=[Depends(check_token)],
)


def get_doctor_repository(
    session: AsyncSession = Depends(get_session),
) -> DoctorRepository:
    return DoctorRepository(session)


def get_specialization_repository(
    session: AsyncSession = Depends(get_session),
) -> SpecializationRepository:
    return SpecializationRepository(session)


@router.get(
    "/",
    response_model=PaginatedDoctorsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_doctors(
    limit: int = Query(100, ge=1, le=100),  # по умолчанию 10, от 1 до 100
    offset: int = Query(0, ge=0),  # по умолчанию 0, не может быть отрицательным
    doctor_repo: DoctorRepository = Depends(get_doctor_repository),
):
    data = await doctor_repo.get_all(offset=offset, limit=limit)
    count = await doctor_repo.get_count()

    return PaginatedDoctorsResponse.model_validate(
        {
            "data": data,
            "total": count,
            "limit": limit,
            "offset": offset,
        }
    )


@router.get(
    "/specialization",
    response_model=PaginatedDoctorSpecializationsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_doctors_specializations(
    limit: int = Query(100, ge=1, le=100),  # по умолчанию 10, от 1 до 100
    offset: int = Query(0, ge=0),  # по умолчанию 0, не может быть отрицательным
    specialization_repo: SpecializationRepository = Depends(
        get_specialization_repository
    ),
):
    data = await specialization_repo.get_all(offset=offset, limit=limit)
    count = await specialization_repo.get_count()

    return PaginatedDoctorSpecializationsResponse.model_validate(
        {
            "data": data,
            "total": count,
            "limit": limit,
            "offset": offset,
        }
    )
