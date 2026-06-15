from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Union, Optional
import jwt

from app.config.config import app_config
from app.schemas.token import TokenSchema
from app.db.models import User


class JWTService:
    def __init__(
        self,
    ):
        self.private_key = app_config.jwt_config.private_key_path.read_text()
        self.public_key = app_config.jwt_config.public_key_path.read_text()
        self.algorithm = app_config.jwt_config.algorithm
        self.access_token_expire_minutes = (
            app_config.jwt_config.access_token_expire_minutes
        )
        self.token_type = app_config.jwt_config.token_type

    def encode(
        self,
        payload: Dict[str, Any],
        expire_timedelta: Optional[timedelta] = None,
    ) -> TokenSchema:
        now = datetime.now(timezone.utc)
        expire = now + (
            expire_timedelta or timedelta(minutes=self.access_token_expire_minutes)
        )

        to_encode = payload.copy()
        to_encode.update(
            exp=expire,
            iat=now,
        )

        token = jwt.encode(
            to_encode,
            self.private_key,
            algorithm=self.algorithm,
        )

        return TokenSchema(token=token, token_type=self.token_type)

    def decode(self, token: Union[str, bytes]) -> Dict[str, Any]:
        return jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm],
        )

    def get_payload(self, user: User):
        return {
            "sub": str(user.id),
            "phone": user.phone,
            "role_id": user.role_id,
        }
