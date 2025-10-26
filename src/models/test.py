from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, func, ForeignKey, Date
from datetime import date
from src.database import Base

class Test(Base):
    __tablename__ = 'tests'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[date] = mapped_column(Date, server_default=func.now())
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    teacher:Mapped["User"] = relationship("User", back_populates="tests")
    test_sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="test")
    question_links: Mapped[list["QuestionTest"]] = relationship("QuestionTest", back_populates="test")