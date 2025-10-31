from pydantic import BaseModel
from typing import Optional

class AnswerCreate(BaseModel):
    text: str
    is_correct: bool = False

class AnswerUpdate(BaseModel):
    text: Optional[str] = None
    is_correct: Optional[bool] = None

class AnswerResponse(BaseModel):
    id: int
    text: str
    order: int
    is_correct: bool
    question_id: int

    class Config:
        from_attributes = True