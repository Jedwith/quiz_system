from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class SessionAnswerCreate(BaseModel):
    question_id: int
    answer_id: Optional[int] = None
    answer_ids: Optional[List[int]] = None
    text: Optional[str] = None

class SessionAnswerResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    student_id: int
    answer_id: Optional[int]
    answer_ids: Optional[List[int]]
    text: Optional[str]
    is_correct: bool
    answered_at: Optional[datetime]

    class Config:
        from_attributes = True
