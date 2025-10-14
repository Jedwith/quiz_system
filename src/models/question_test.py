from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from src.database import Base

class QuestionTest(Base):
    __tablename__ = 'question_test'

    order: Mapped[int] = mapped_column(Integer, nullable=True)
    points: Mapped[int] = mapped_column(default=1)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), index=True, primary_key=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), index=True, primary_key=True)

    question: Mapped["Question"] = relationship("Question", back_populates="question_links")
    test: Mapped["Test"] = relationship("Test", back_populates="question_links")