from fastapi import APIRouter
from app.core.config import routes

patient_router = APIRouter(prefix=routes.patient, tags=["Patient"])
