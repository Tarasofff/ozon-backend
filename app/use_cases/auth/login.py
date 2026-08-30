from app.database.models import User


class AuthenticateUserUseCase:
    def get_payload(self, user: User):
        return {
            "sub": str(user.id),
            "phone": user.phone,
            "role": user.role,
        }
