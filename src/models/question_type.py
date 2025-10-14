from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from src.database import Base

class QuestionType(Base):
    __tablename__ = 'question_types'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    description: Mapped[str]

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="type")
