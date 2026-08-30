from datetime import date, datetime
from enum import StrEnum
from typing import Any
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import field_validator
from sqlalchemy import Enum


@asynccontextmanager
async def log_registered_routes(app: FastAPI):
    print("\n📌 Registered routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            print(f"{methods:10s} | {route.path}")
    print()
    yield


def get_current_date():
    today = datetime.today()
    return today.strftime("%d.%m.%Y")


def to_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Неверный формат даты")


class DateParser:
    @field_validator("date_of_birth", mode="before")
    @staticmethod
    def parse(dob: Any) -> date | None:
        if isinstance(dob, str):
            try:
                return to_date(dob)
            except ValueError:
                return None
        elif isinstance(dob, date):
            return dob
        return None


def enum_values(enum_class: type[StrEnum]) -> list[str]:
    return [member.value for member in enum_class]
