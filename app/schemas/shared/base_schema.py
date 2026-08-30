from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        # Автоматически удаляет " " по краям во всех str-полях проекта
        str_strip_whitespace=True,
    )
