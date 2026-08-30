from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.enums.table_names import TableNames
from app.database.models.enums.user_role import UserRole
from app.database.models.user import User

if TYPE_CHECKING:
    from app.database.models import Session


class Nurse(User):
    __tablename__ = TableNames.NURSE

    id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.USER}.id", ondelete="CASCADE"), primary_key=True
    )

    sessions: Mapped[list[Session]] = relationship("Session", back_populates="nurse")

    __mapper_args__ = {
        "polymorphic_identity": UserRole.NURSE,
    }
