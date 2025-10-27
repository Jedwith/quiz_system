from pydantic import BaseModel
from typing import Optional

class QuestionCreate(BaseModel):
    text: str
    type_id: int

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    type_id: Optional[int] = None

class QuestionResponse(BaseModel):
    id: int
    text: str
    type_id: int

    class Config:
        from_attributes = True


class QuestionCreateInTest(BaseModel):
    text: str
    type_id: int
    order: Optional[int] = None
    points: int = 1

class QuestionAddToTest(BaseModel):
    order: Optional[int] = None
    points: int = 1

class QuestionInTestResponse(BaseModel):
    id: int
    text: str
    type_id: int
    order: Optional[int] = None
    points: int

    class Config:
        from_attributes = True
