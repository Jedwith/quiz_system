from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from src.database import Base

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    text: Mapped[str]
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('question_types.id'), index=True)

    answers_in_session: Mapped[list["SessionAnswer"]] = relationship("SessionAnswer", back_populates="question")
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="question")
    type:Mapped["QuestionType"] = relationship("QuestionType", back_populates="questions")
    question_links: Mapped[list["QuestionTest"]] = relationship("QuestionTest", back_populates="question")