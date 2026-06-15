from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import PatientDoctorDiagnose


class PatientDoctorDiagnoseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> PatientDoctorDiagnose | None:
        stmt = select(PatientDoctorDiagnose).where(PatientDoctorDiagnose.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        patient_id: int,
        doctor_id: int,
        diagnose_id: int,
        planned_session_count: int = 0,
    ) -> PatientDoctorDiagnose:
        value = PatientDoctorDiagnose(
            patient_id=patient_id,
            doctor_id=doctor_id,
            diagnose_id=diagnose_id,
            planned_session_count=planned_session_count,
        )
        self.session.add(value)
        await self.session.flush()
        return value
