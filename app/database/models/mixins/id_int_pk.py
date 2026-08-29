from sqlalchemy.orm import Mapped, mapped_column, declarative_mixin


@declarative_mixin
class IdIntPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
