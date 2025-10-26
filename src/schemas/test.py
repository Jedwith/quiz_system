from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date as DateType

class TestCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TestResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: DateType
    teacher_id: int

    class Config:
        from_attributes = True