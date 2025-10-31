from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.answer import AnswerCreate, AnswerUpdate, AnswerResponse
from src.services import answer_service
from src.core.dependencies import get_teacher_id

router = APIRouter(prefix="/questions", tags=["Answers"])

@router.get(
    "/{question_id}/answers",
    response_model=List[AnswerResponse],
    summary="Получение всех вариантов ответа к тесту"
)
async def get_question_answers(question_id: int, teacher_id: int = Depends(get_teacher_id),  db: AsyncSession = Depends(get_db)):
    return await answer_service.get_answers_by_question(db, question_id, teacher_id)

@router.post(
    "/{question_id}/answers",
    response_model=AnswerResponse,
    summary="Создание нового варианта ответа к вопросу"
)
async def create_answer(answer: AnswerCreate, question_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await answer_service.create_answer(db, question_id, answer, teacher_id)

@router.patch(
    "/answers/{answer_id}",
    response_model=AnswerResponse,
    summary="Редактирование варианта ответа"
)
async def update_answer(answer: AnswerUpdate, answer_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await answer_service.update_answer(db, answer_id, answer, teacher_id)

@router.delete(
    "/answers/{answer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление варианта ответа"
)
async def delete_answer(answer_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await answer_service.delete_answer(db, answer_id, teacher_id)

