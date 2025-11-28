from dataclasses import Field
from datetime import date as DateType, datetime
from pydantic import BaseModel
from typing import Literal, Optional, List

class UserInfo(BaseModel):
    id: int
    name: str
    role: str
    first_name: str
    last_name: str


class QuestionData(BaseModel):
    id: int
    text: str
    type_id: int
    order: int
    points: int


class TestData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    questions: List[QuestionData] = Field(default_factory=list)


class SessionInfo(BaseModel):
    session_id: int
    test_id: int
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    test_name: str
    test_description: Optional[str] = None
    total_questions: int
    questions: List[QuestionData]
    # room_code: str


