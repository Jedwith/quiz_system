from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from src.database import Base

class ClassType(Base):
    __tablename__ = 'class_types'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]

    sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="type")
    attendances: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="type")

