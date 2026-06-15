from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from app.config.config import app_config


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=app_config.database_config.postgres_naming_convention
    )

    def __repr__(self) -> str:
        columns = ", ".join(
            [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]
        )
        return f"<{self.__class__.__name__}({columns})>"
