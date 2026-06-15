from fastapi import APIRouter
from app.api.controllers import (
    user_router,
    patient_router,
    doctor_router,
    diagnose_router,
)

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(patient_router)
api_router.include_router(doctor_router)
api_router.include_router(diagnose_router)
