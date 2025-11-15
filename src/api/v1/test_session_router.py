from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.test_session import TestSessionCreate, TestSessionResponse
from src.schemas.session_answer import SessionAnswerCreate, SessionAnswerResponse
from src.services import test_session_service, session_answer_service
from src.core.dependencies import get_teacher_id, get_student_id

router = APIRouter(prefix="/sessions", tags=["Test Sessions"])

@router.post("/rooms/{room_code}/session", response_model=TestSessionResponse, summary="Создание сессии")
async def create_test_session(session: TestSessionCreate, room_code: str, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_session_service.create_test_session(db, session, room_code, teacher_id)

@router.post("/{session_id}/finish", status_code=status.HTTP_200_OK, summary="Завершение сессии")
async def finish_test_session(session_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_session_service.finish_test_session(db, session_id, teacher_id)

@router.post("/{session_id}/answers", response_model=SessionAnswerResponse, summary="Отправка ответа студентом в сессии")
async def submit_answer(session_id: int, answer_data: SessionAnswerCreate, student_id: int = Depends(get_student_id), db: AsyncSession = Depends(get_db)):
    return await session_answer_service.save_student_answer(db, answer_data, session_id, student_id)
