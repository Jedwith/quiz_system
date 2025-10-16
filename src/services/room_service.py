import string
import random
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.room import Room
from src.models.user import User
from sqlalchemy import select
from src.schemas.room import RoomCreate, RoomUpdate
from fastapi import HTTPException, status

async def generate_unique_room_code(db: AsyncSession, length: int = 6) -> str:
    """Генерирует уникальный код комнаты асинхронно."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        # Асинхронный запрос для проверки уникальности
        result = await db.execute(select(Room).filter(Room.code == code))
        if not result.scalars().first():
            return code

async def create_room(db: AsyncSession, room_data:RoomCreate):
    result = await db.execute(select(User).where(User.id == room_data.teacher_id))
    teacher = result.scalar_one_or_none()

    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")

    code = await generate_unique_room_code(db)

    room = Room(
        name=room_data.name,
        code=code,
        teacher_id=room_data.teacher_id,
        status='active'

    )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room







