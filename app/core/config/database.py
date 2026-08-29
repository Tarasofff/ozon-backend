from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = ".env"


class DatabaseConfig(BaseSettings):
    user: str = ""
    password: str = ""
    port: int = 5432
    host: str = ""
    db: str = ""

    naming_convention: dict[str, str] = {
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


database_config = DatabaseConfig()
