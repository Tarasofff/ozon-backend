from datetime import datetime
from app.schemas.shared.base_read import BaseRead


class BaseTimestampedRead(BaseRead):
    created_at: datetime
    updated_at: datetime
