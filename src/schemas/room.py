from datetime import date as DateType

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RoomCreate(BaseModel):
    name: str
    teacher_id: int
    status: str = 'active'


class RoomResponse(BaseModel):
    id: int
    name: str
    code: str
    status: str
    created_at: DateType
    teacher_id: int

    class Config:
        from_attributes = True
