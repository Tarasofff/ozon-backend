# def get_current_date():
#     today = datetime.today()
#     return today.strftime("%d.%m.%Y")


# def to_date(date_str: str) -> date:
#     try:
#         return datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         pass
#     try:
#         return datetime.strptime(date_str, "%d.%m.%Y").date()
#     except ValueError:
#         raise ValueError("Неверный формат даты")


# class DateParser:
#     @field_validator("date_of_birth", mode="before")
#     @staticmethod
#     def parse(dob: Any) -> date | None:
#         if isinstance(dob, str):
#             try:
#                 return to_date(dob)
#             except ValueError:
#                 return None
#         elif isinstance(dob, date):
#             return dob
#         return None
