from pydantic import BaseModel
from pathlib import Path
from app.core.constants import BASE_DIR


class JwtConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1440  # 1440 24h
    token_type: str = "Bearer"


jwt_config = JwtConfig()
