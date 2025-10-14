from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey
from src.database import Base

class Answer(Base):
    __tablename__ = 'answers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    text: Mapped[str]
    order: Mapped[int] = mapped_column(Integer, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'))

    answers_in_session: Mapped[list["SessionAnswer"]] = relationship("SessionAnswer", back_populates="answer")
    question: Mapped["Question"] = relationship("Question", back_populates="answers")