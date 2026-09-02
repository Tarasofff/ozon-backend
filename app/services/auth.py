from app.core.exceptions import InvalidCredentialsException
from app.database.models.enums.user_role import UserRole
from app.database.models.user import User
from app.infrastructure.security.hash import validate_password
from app.infrastructure.security.jwt import encode_token
from app.repository import UserRepository
from app.schemas import AccessTokenPayload, AuthPayload
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import AccessToken


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session=session)

    def _get_token_payload(
        self, user_id: int, user_role: UserRole
    ) -> AccessTokenPayload:
        return {
            "user_id": user_id,
            "user_role": user_role.value,
        }

    def _get_access_token(self, user_id: int, user_role: UserRole):
        payload = self._get_token_payload(user_id, user_role)
        return encode_token(payload)

    async def _check_user_credentials(self, auth_payload: AuthPayload):
        user = await self.user_repo.get_by_phone(auth_payload.phone)
        if user:
            compare_password = validate_password(
                auth_payload.password, user.password_hash
            )
            if compare_password:
                return user

        raise InvalidCredentialsException()

    async def login(self, auth_payload: AuthPayload) -> tuple[User, AccessToken]:
        user = await self._check_user_credentials(auth_payload)
        access_token = self._get_access_token(user_id=user.id, user_role=user.role)
        return user, access_token
