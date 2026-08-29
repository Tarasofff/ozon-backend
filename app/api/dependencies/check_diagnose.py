from fastapi import Depends
from app.api.exceptions.api_exceptions import UnprocessableEntityException
from app.database.session import get_session
from app.repository import DiagnoseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.diagnose import DiagnoseCreate


def get_diagnose_repo(
    session: AsyncSession = Depends(get_session),
) -> DiagnoseRepository:
    return DiagnoseRepository(session=session)


async def check_diagnose_exists_by_name(
    diagnose: DiagnoseCreate, diagnose_repo: DiagnoseRepository = Depends(get_diagnose_repo)
):
    diagnose_validate = DiagnoseCreate.model_validate(diagnose)

    result = await diagnose_repo.get_by_name(diagnose_validate.name)
    if result:
        raise UnprocessableEntityException(f"Diagnose {diagnose_validate.name} already exists")

    return diagnose_validate
