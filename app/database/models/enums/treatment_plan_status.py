from enum import StrEnum, auto


class TreatmentPlanStatus(StrEnum):
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()
