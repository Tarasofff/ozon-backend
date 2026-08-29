from pydantic import BaseModel


class AppRoutes(BaseModel):
    prefix: str = "/v1"

    nurse: str = "/nurse"
    doctor: str = "/doctor"
    patient: str = "/patient"
    user: str = "/user"
    diagnose: str = "/diagnose"


app_routes = AppRoutes()
