from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Test, Question, QuestionTest, Room, TestSession
from src.schemas.test_session import TestSessionCreate, TestSessionResponse
from sqlalchemy import select
from fastapi import HTTPException, status

async def create_test_session(db: AsyncSession, test_session_data: TestSessionCreate, room_code: str, teacher_id: int):
    result = await db.execute(select(Room).where(Room.code == room_code, Room.teacher_id == teacher_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комната не найдена или у вас нет прав доступа"
        )

    result = await db.execute(select(Test).where(Test.id == test_session_data.test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тест не найден"
        )

    session = TestSession(
        room_id=room.id,
        test_id=test_session_data.test_id,
        type_id=test_session_data.type_id,
        start_time=datetime.now(timezone.utc)
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return TestSessionResponse(
        id=session.id,
        start_time=session.start_time,
        room_code=room_code,
        test_title=test.name
    )

async def finish_test_session(db: AsyncSession, session_id: int, teacher_id: int):
    result = await db.execute(
        select(TestSession)
        .join(Room)
        .where(TestSession.id == session_id, Room.teacher_id == teacher_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не найдена или у вас нет прав доступа"
        )
    if session.end_time is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сессия уже завершена"
        )
    session.end_time = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Сессия успешно завершена"}







