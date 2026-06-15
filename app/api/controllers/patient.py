from typing import Optional
from fastapi.responses import StreamingResponse
from app.api.dependencies.check_patient_exists import check_patient_exists_by_phone
from app.api.dependencies.check_user_rules import check_user_doctor_role
from app.config.config import app_config
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.repository.patient import PatientRepository
from app.schemas.patient import (
    PatientCreate,
    PatientRead,
    PatientUpdate,
    PaginatedPatientsResponse,
)
from app.services import PatientService, ReportService
from app.api.dependencies import (
    check_patient_exists_by_id,
    check_hospital_exists,
    check_patient_doctor_diagnose_exists,
    check_token,
)

router = APIRouter(
    prefix=app_config.api_v1_prefix.patient,
    tags=["Patients"],
    dependencies=[Depends(check_token)],
)


def get_patient_repository(
    session: AsyncSession = Depends(get_session),
) -> PatientRepository:
    return PatientRepository(session)


def get_patient_service(
    session: AsyncSession = Depends(get_session),
) -> PatientService:
    return PatientService(session)


def get_report_service(session: AsyncSession = Depends(get_session)) -> ReportService:
    return ReportService(session=session)


@router.post(
    "/create",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(check_user_doctor_role),
        Depends(check_patient_exists_by_phone),
    ],
)
async def create(
    patient_data: PatientCreate,
    patient_service: PatientService = Depends(get_patient_service),
):
    return await patient_service.create(patient_data)


@router.get(
    "/filter",
    status_code=status.HTTP_200_OK,
)
async def get_by_filter(
    id: Optional[int] = None,
    last_name: Optional[str] = None,
    first_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    phone: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[str] = None,
    limit: int = Query(15, ge=1, le=15),  # по умолчанию 15, от 1 до 15
    offset: int = Query(0, ge=0),  # по умолчанию 0, не может быть отрицательным
    patient_repo: PatientRepository = Depends(get_patient_repository),
):
    data = await patient_repo.get_by_filter(
        id=id,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        phone=phone,
        date_of_birth=date_of_birth,
        email=email,
        is_active=(
            True
            if is_active and is_active.lower() == "true"
            else False if is_active and is_active.lower() == "false" else None
        ),
    )

    total = len(data)

    return PaginatedPatientsResponse.model_validate(
        {
            "data": data,
            "total": total,
            "limit": limit,
            "offset": offset,
        }
    )


@router.get(
    "/detail/id/{patient_id}",
    # response_model=PatientReadSchema, #TODO
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_patient_exists_by_id)],
)
async def get_by_id(
    patient_id: int,
    patient_repo: PatientRepository = Depends(get_patient_repository),
):
    return await patient_repo.get_by_id(patient_id, True)


@router.put(
    "/update/{patient_id}",
    response_model=PatientRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_patient_exists_by_id)],
)
async def update(
    patient_data: PatientUpdate,
    patient_id: int,
    patient_repo: PatientRepository = Depends(get_patient_repository),
):
    patient = patient_data.model_dump()
    return await patient_repo.update(patient_id, patient)


@router.get(
    "/report",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
)
async def get_report(
    patient_id: int = Depends(check_patient_exists_by_id),
    hospital_id: int = Depends(check_hospital_exists),
    patient_doctor_diagnose_id: int = Depends(check_patient_doctor_diagnose_exists),
    disposition: str = Query("inline", regex="^(inline|attachment)$"),
    report_service: ReportService = Depends(get_report_service),
):
    print(patient_id, hospital_id, patient_doctor_diagnose_id, disposition)
    report_data_dump = await report_service.get_report_data(
        patient_id, hospital_id, patient_doctor_diagnose_id
    )

    pdf_bytes = await report_service.get_pdf_bytes(report_data_dump)

    media_type = "application/pdf"
    file_ext = "pdf"
    filename = f"report_patient_id_{patient_id}.{file_ext}"
    headers = {"Content-Disposition": f"{disposition}; filename={filename}"}

    return StreamingResponse(
        pdf_bytes,
        media_type=media_type,
        headers=headers,
    )
