from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, func, ForeignKey
from datetime import datetime
from src.database import Base

class TestSession(Base):
    __tablename__ = 'test_sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'), index=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), index=True)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('class_types.id'), index=True)

    room:Mapped["Room"] = relationship("Room", back_populates="test_sessions")
    test:Mapped["Test"] = relationship("Test", back_populates="test_sessions")
    type:Mapped["ClassType"] = relationship("ClassType", back_populates="sessions")
    answers_in_session: Mapped[list["SessionAnswer"]] = relationship("SessionAnswer", back_populates="session")
    attendances: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="session")
