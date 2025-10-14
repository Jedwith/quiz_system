from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from src.database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50),nullable=False)
    last_name: Mapped[str] = mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String(150),nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'))

    role: Mapped["Role"] = relationship("Role", back_populates="users")
    rooms: Mapped[list["Room"]] = relationship("Room", back_populates="teacher")
    tests: Mapped[list["Test"]] = relationship("Test", back_populates="teacher")
    answers_in_session: Mapped[list["SessionAnswer"]] = relationship("SessionAnswer", back_populates="student")
    attendances: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="student")
