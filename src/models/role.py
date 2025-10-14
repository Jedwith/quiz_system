from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from src.database import Base

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]

    users: Mapped[list["User"]] = relationship("User", back_populates="role")