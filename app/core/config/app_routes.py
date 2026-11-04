from pydantic import BaseModel


class AppRoutes(BaseModel):
    prefix: str = "/v1"

    patient: str = "/patient"
    user: str = "/user"
    auth: str = "/auth"


app_routes = AppRoutes()
