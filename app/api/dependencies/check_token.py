from app.api.exceptions.api_exceptions import UnauthorizedException
from app.services.jwt import JWTService
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()


def get_jwt_service() -> JWTService:
    return JWTService()


async def check_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    try:
        token = credentials.credentials
        return jwt_service.decode(token)
    except Exception:
        raise UnauthorizedException("Invalid token")
