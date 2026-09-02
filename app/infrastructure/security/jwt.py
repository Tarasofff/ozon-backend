from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import jwt

from app.core.config import jwt_config
from app.schemas import AccessToken, AccessTokenPayload, EncodedAccessTokenPayload

_PRIVATE_KEY = jwt_config.private_key_path.read_text()
_PUBLIC_KEY = jwt_config.public_key_path.read_text()
_ALGORITHM = jwt_config.algorithm
_EXPIRE_MINUTES = jwt_config.access_token_expire_minutes
_TOKEN_TYPE = jwt_config.token_type


def encode_token(
    payload: AccessTokenPayload,
    expire_timedelta: Optional[timedelta] = None,
) -> AccessToken:
    now = datetime.now(timezone.utc)
    expire = now + (expire_timedelta or timedelta(minutes=_EXPIRE_MINUTES))

    to_encode = {
        **payload,
        "exp": expire,
        "iat": now,
    }

    encoded_jwt = jwt.encode(to_encode, _PRIVATE_KEY, algorithm=_ALGORITHM)
    return AccessToken(access_token=encoded_jwt, token_type=_TOKEN_TYPE)


def decode_token(token: Union[str, bytes]) -> EncodedAccessTokenPayload:
    return jwt.decode(token, _PUBLIC_KEY, algorithms=[_ALGORITHM])
