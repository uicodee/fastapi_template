from datetime import datetime

from pydantic import BaseModel


def serialize_time(value: datetime) -> str:
    return value.strftime('%d.%m.%Y %H:%M')


class Base(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: serialize_time
        }
        orm_mode = True

