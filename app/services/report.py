from pathlib import Path
from io import BytesIO
from typing import Any
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import select
from weasyprint import HTML  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import (
    Hospital,
    Address,
    PatientDoctorDiagnose,
    Doctor,
    User,
    Session,
    Post,
    Cabinet,
    Nurse,
)
from app.db.models.diagnose import Diagnose
from app.repository import HospitalRepository, PatientRepository
from app.schemas.report import (
    HospitalSchema,
    PatientDoctorDiagnoseSchema,
    PatientReportSchema,
    PatientSchema,
    PatientSessionListSchema,
)
from sqlalchemy.orm import selectinload, load_only
from app.utils.utils import get_current_date

BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "templates"
report_filename = "report.html"
env = Environment(loader=FileSystemLoader(templates_dir))


class ReportService:
    def __init__(self, session: AsyncSession):
        self.template_env = env
        self.report_filename = report_filename
        self.base_dir = BASE_DIR
        self.session = session
        self.patient_repo = PatientRepository(session=session)
        self.hospital_repo = HospitalRepository(session=session)

    async def _get_session_data(
        self, patient_doctor_diagnose_id: int, hospital_id: int
    ):
        stmt = (
            select(Session)
            .join(Session.post)
            .join(Post.cabinet)
            .join(Cabinet.hospital)
            .where(Session.patient_doctor_diagnose_id == patient_doctor_diagnose_id)
            .where(Hospital.id == hospital_id)
            .options(
                load_only(
                    Session.id,
                    Session.notes,
                    Session.session_duration_ms,
                    Session.ozone_concentration,
                    Session.is_active,
                    Session.created_at,  # type: ignore
                    Session.updated_at,  # type: ignore
                ),
                selectinload(Session.post)
                .joinedload(Post.cabinet)
                .load_only(Cabinet.id, Cabinet.number),
                selectinload(Session.nurse)
                .joinedload(Nurse.user)
                .load_only(
                    User.id,
                    User.first_name,
                    User.middle_name,
                    User.last_name,
                    User.phone,
                ),
            )
            .order_by(Session.id)
        )

        result = await self.session.execute(stmt)
        session_data = result.scalars().all()
        return PatientSessionListSchema.model_validate(
            {"session": session_data}
        ).model_dump()

    async def _get_patient_doctor_diagnose_data(self, patient_doctor_diagnose_id: int):
        stmt = (
            select(PatientDoctorDiagnose)
            .where(PatientDoctorDiagnose.id == patient_doctor_diagnose_id)
            .options(
                selectinload(PatientDoctorDiagnose.diagnose).load_only(
                    Diagnose.id, Diagnose.name
                ),
                selectinload(PatientDoctorDiagnose.doctor)
                .joinedload(Doctor.user)
                .load_only(
                    User.id,
                    User.first_name,
                    User.middle_name,
                    User.last_name,
                    User.phone,
                ),
            )
        )

        result = await self.session.execute(stmt)
        patient_doctor_diagnose_data = result.scalar_one_or_none()

        return PatientDoctorDiagnoseSchema.model_validate(
            patient_doctor_diagnose_data
        ).model_dump()

    async def _get_hospital_data(self, hospital_id: int):

        stmt = (
            select(Hospital)
            .where(Hospital.id == hospital_id)
            .options(
                selectinload(Hospital.address).load_only(
                    Address.id,
                    Address.country_name,
                    Address.city_name,
                    Address.street_name,
                    Address.building_number,
                    Address.postal_code,
                )
            )
        )
        result = await self.session.execute(stmt)
        hospital_data = result.scalar_one_or_none()

        return HospitalSchema.model_validate(hospital_data).model_dump()

    async def get_report_data(
        self, patient_id: int, hospital_id: int, patient_doctor_diagnose_id: int
    ):
        patient_dump = await self._get_patient_data(patient_id)

        session_dump = await self._get_session_data(
            patient_doctor_diagnose_id, hospital_id
        )

        hospital_dump = await self._get_hospital_data(hospital_id)

        patient_doctor_diagnose_dump = await self._get_patient_doctor_diagnose_data(
            patient_doctor_diagnose_id
        )

        return PatientReportSchema.model_validate(
            {
                "patient": patient_dump,
                "hospital": hospital_dump,
                **session_dump,
                **patient_doctor_diagnose_dump,
            }
        ).model_dump()

    async def _get_patient_data(self, patient_id: int):
        patient_data = await self.patient_repo.get_by_id(patient_id)

        return PatientSchema.model_validate(patient_data).model_dump()

    async def get_pdf_bytes(self, report: dict[str, Any]):
        # Рендерим HTML
        template = self.template_env.get_template(self.report_filename)

        date = get_current_date()

        html_content = template.render(
            report=report,
            date=date,
        )

        # Генерация PDF в памяти
        pdf_bytes = BytesIO()
        HTML(string=html_content, base_url=str(self.base_dir)).write_pdf(pdf_bytes)  # type: ignore
        pdf_bytes.seek(0)
        return pdf_bytes
