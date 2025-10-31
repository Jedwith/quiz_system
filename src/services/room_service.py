import string
import random
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Room
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

async def get_rooms(db: AsyncSession, teacher_id: int):
    result = await db.execute(
        select(Room)
        .where(Room.teacher_id == teacher_id)
        .order_by(Room.created_at.desc())  # новые комнаты первыми
    )
    rooms = result.scalars().all()
    return rooms

async def create_room(db: AsyncSession, room_data:RoomCreate, teacher_id: int):
    code = await generate_unique_room_code(db)
    room = Room(
        name=room_data.name,
        code=code,
        teacher_id=teacher_id,
        status='active'
    )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

async def update_room(db: AsyncSession, room_id:int, room_data:RoomUpdate, teacher_id:int):
    result = await db.execute(select(Room).where(Room.id == room_id, Room.teacher_id == teacher_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена или у вас нет прав на ее редактирование")

    if room_data.name is not None:
        room.name = room_data.name

    await db.commit()
    await db.refresh(room)
    return room

async def delete_room(db: AsyncSession, room_id, teacher_id:int):
    result = await db.execute(select(Room).where(Room.id == room_id, Room.teacher_id == teacher_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена или у вас нет прав на ее удаление")

    await db.delete(room)
    await db.commit()






