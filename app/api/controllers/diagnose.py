from fastapi import APIRouter, Depends, Query, status
from app.api.dependencies import check_token
from app.api.dependencies.check_diagnose import check_diagnose_exists_by_name
from app.config.config import app_config
from app.db.session import get_session
from app.repository import DiagnoseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.diagnose import (
    PaginatedDiagnosesResponse,
    DiagnoseCreate,
    DiagnoseRead,
)

router = APIRouter(
    prefix=app_config.api_v1_prefix.diagnose,
    tags=["Diagnoses"],
    dependencies=[Depends(check_token)],
)


def get_diagnose_repository(
    session: AsyncSession = Depends(get_session),
) -> DiagnoseRepository:
    return DiagnoseRepository(session)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=DiagnoseRead,
    dependencies=[Depends(check_diagnose_exists_by_name)],
)
async def create(
    diagnose: DiagnoseCreate,
    diagnose_repo: DiagnoseRepository = Depends(get_diagnose_repository),
):
    result = await diagnose_repo.create(diagnose.name)
    await diagnose_repo.session.commit()
    return result


@router.get(
    "/",
    response_model=PaginatedDiagnosesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all(
    limit: int = Query(100, ge=1, le=100),  # по умолчанию 10, от 1 до 100
    offset: int = Query(0, ge=0),  # по умолчанию 0, не может быть отрицательным
    diagnose_repo: DiagnoseRepository = Depends(get_diagnose_repository),
):
    data = await diagnose_repo.get_all(offset=offset, limit=limit)
    count = await diagnose_repo.get_count()

    return PaginatedDiagnosesResponse.model_validate(
        {
            "data": data,
            "total": count,
            "limit": limit,
            "offset": offset,
        }
    )
