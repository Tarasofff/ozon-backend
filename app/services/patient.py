from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Patient
from app.repository import PatientRepository, PatientDoctorDiagnoseRepository, DoctorRepository
from app.schemas.patient import PatientCreateSchema


class PatientService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.patient_repo = PatientRepository(session=session)
        self.pdd_repo = PatientDoctorDiagnoseRepository(session=session)
        self.doctor_repo = DoctorRepository(session=session)

    async def create(self, patient_data: PatientCreateSchema):
        patient_data_dump = patient_data.model_dump()

        patient_model = Patient(
            first_name=patient_data_dump["first_name"],
            middle_name=patient_data_dump["middle_name"],
            last_name=patient_data_dump["last_name"],
            phone=patient_data_dump["phone"],
            date_of_birth=patient_data_dump["date_of_birth"],
            email=patient_data_dump.get("email"),
            notes=patient_data_dump.get("notes"),
        )

        created_patient = await self.patient_repo.create(patient_model)

        doctor = await self.doctor_repo.get_doctor_by_user_id(patient_data_dump["user_id"])

        if patient_data.diagnose_ids and doctor:
            for diagnose in patient_data.diagnose_ids:
                await self.pdd_repo.create(created_patient.id, doctor.id, diagnose.id, diagnose.planned_session_count)

        await self.session.commit()

        return created_patient
