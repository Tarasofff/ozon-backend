from app.database.models import Patient
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PatientRepository(BaseRepository[Patient]):
    def __init__(self, session: AsyncSession):
        super().__init__(Patient, session)
