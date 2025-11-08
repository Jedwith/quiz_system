from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TestSessionCreate(BaseModel):
    test_id: int
    type_id: int

class TestSessionResponse(BaseModel):
    id: int
    start_time: Optional[datetime]
    room_code: str
    test_title: str

    class Config:
        from_attributes = True
