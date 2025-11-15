from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, func, ForeignKey
from datetime import datetime
from src.database import Base

class SessionAnswer(Base):
    __tablename__ = 'session_answers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    text: Mapped[str | None] = mapped_column(String, )
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey('test_sessions.id'), index=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    answer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('answers.id'), index=True)

    student: Mapped["User"] = relationship("User", back_populates="answers_in_session")
    session: Mapped["TestSession"] = relationship("TestSession", back_populates="answers_in_session")
    question: Mapped["Question"] = relationship("Question", back_populates="answers_in_session")
    answer: Mapped["Answer"] = relationship("Answer", back_populates="answers_in_session")