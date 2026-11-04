from enum import StrEnum


def enum_values(enum_class: type[StrEnum]) -> list[str]:
    return [member.value for member in enum_class]
