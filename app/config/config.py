from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, EmailStr
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

env_file = ".env"


class JwtConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1440  # 1440 24h
    token_type: str = "Bearer"


class ApiV1Prefix(BaseModel):
    global_prefix: str = "/v1"
    nurse: str = "/nurse"
    doctor: str = "/doctor"
    patient: str = "/patient"
    user: str = "/user"
    diagnose: str = "/diagnose"


class UserRole:
    ADMIN: str = "admin"
    NURSE: str = "nurse"
    DOCTOR: str = "doctor"

    @classmethod
    def list(cls) -> list[str]:
        return [
            value
            for key, value in vars(cls).items()
            if key.isupper() and isinstance(value, str)
        ]


class UserAdminConfig(BaseSettings):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    phone: str = ""
    email: EmailStr = "example@email.com"
    password: str = ""
    date_of_birth: str = "03.12.2000"

    model_config = SettingsConfigDict(
        env_prefix="USER_ADMIN_", env_file=env_file, extra="allow"
    )


class DatabaseConfig(BaseSettings):
    user: str = ""
    password: str = ""
    port: int = 5432
    host: str = ""
    db: str = ""

    postgres_naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s",
        "pk": "pk_%(table_name)s",
    }

    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", env_file=env_file, extra="allow"
    )


class AppConfig(BaseSettings):
    app_name: str = "Ozon"
    debug: bool = False
    api_v1_prefix: ApiV1Prefix = ApiV1Prefix()
    jwt_config: JwtConfig = JwtConfig()
    user_role: UserRole = UserRole()
    user_admin_config: UserAdminConfig = UserAdminConfig()
    database_config: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(env_file=env_file, extra="allow")


app_config = AppConfig()
