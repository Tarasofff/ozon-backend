from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.table_names import TableNames
from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, IdIntPkMixin
from app.config.config import app_config

if TYPE_CHECKING:
    from app.db.models import User

roles_str = ", ".join(f"'{role}'" for role in app_config.user_role.list())


class Role(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.ROLE

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    user: Mapped[list[User]] = relationship(back_populates="role")

    __table_args__ = (CheckConstraint(f"name IN ({roles_str})", name="list"),)
