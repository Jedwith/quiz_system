from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, func, ForeignKey, Date
from datetime import date
from src.database import Base

class Room(Base):
    __tablename__ = 'rooms'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    created_at: Mapped[date] = mapped_column(Date, server_default=func.now())
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    teacher:Mapped["User"] = relationship("User", back_populates="rooms")
    test_sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="room")