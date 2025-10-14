from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey, String
from src.database import Base

class Attendance(Base):
    __tablename__ = 'attendances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="attended")
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey('test_sessions.id'), index=True)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('class_types.id'), index=True)

    student:Mapped["User"] = relationship("User", back_populates="attendances")
    session:Mapped["TestSession"] = relationship("TestSession", back_populates="attendances")
    type:Mapped["ClassType"] = relationship("ClassType", back_populates="attendances")