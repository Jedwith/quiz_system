from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.room import RoomCreate, RoomResponse
from src.services import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomResponse, summary="Создание комнаты")
async def create_room(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    return await room_service.create_room(db, room)

