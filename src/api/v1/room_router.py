from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from src.services import room_service
from src.core.dependencies import get_teacher_id

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=List[RoomResponse], summary="Получение комнат преподавателя")
async def get_rooms(teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await room_service.get_rooms(db, teacher_id)
@router.post("/", response_model=RoomResponse, summary="Создание комнаты")
async def create_room(room: RoomCreate, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await room_service.create_room(db, room, teacher_id)

@router.patch("/{room_id}", response_model=RoomResponse, summary="Редактирование комнаты")
async def update_room(room: RoomUpdate, room_id: int = Path(..., gt=0), teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await room_service.update_room(db, room_id, room, teacher_id)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление комнаты")
async def delete_room(room_id: int = Path(..., gt=0), teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await room_service.delete_room(db, room_id, teacher_id)

