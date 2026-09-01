from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    name: str = "Ozon"
    environment: str = "dev"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def is_dev(self) -> bool:
        return self.environment == "dev"


app_config = AppConfig()
