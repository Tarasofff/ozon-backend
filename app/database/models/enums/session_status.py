from enum import StrEnum, auto


class SessionStatus(StrEnum):
    PLANNED = auto()  # "planned" - запланирована/создана в графике
    IN_PROGRESS = auto()  # "in_progress" - процедура идет прямо сейчас
    COMPLETED = auto()  # "completed" - успешно проведена
    CANCELLED = auto()  # "cancelled" - отменена (пациент не пришел / отмена)
