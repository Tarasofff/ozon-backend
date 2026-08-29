from app.api.dependencies.check_patient_exists import (
    check_patient_exists_by_id,
    check_patient_exists_by_phone,
)
from app.api.dependencies.check_hospital_exists import check_hospital_exists
from app.api.dependencies.check_treatment_plan_exists import (
    check_treatment_plan_exists,
)
from app.api.dependencies.check_login_user import check_login_user
from app.api.dependencies.check_register_user import check_register_user
from app.api.dependencies.check_token import check_token
from app.api.dependencies.check_user_rules import check_user_doctor_role
from app.api.dependencies.check_diagnose import check_diagnose_exists_by_name
