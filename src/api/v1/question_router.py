from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.question import QuestionCreateInTest, QuestionAddToTest, QuestionInTestResponse
from src.services import test_service, question_service
from src.core.dependencies import get_teacher_id

router = APIRouter(prefix="/tests", tags=["Questions"])

@router.get("/{test_id}/questions", response_model=List[QuestionInTestResponse], summary="Получение вопросов теста")
async def get_test_questions(test_id: int, teacher_id: int = Depends(get_teacher_id),  db: AsyncSession = Depends(get_db)):
    return await question_service.get_test_questions(db, test_id, teacher_id)

@router.post("/{test_id}/questions", response_model=QuestionInTestResponse, summary="Создание вопроса в тесте")
async def create_question_in_test(question: QuestionCreateInTest, test_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await question_service.create_question_in_test(db, question, test_id, teacher_id)

@router.post("/{test_id}/questions/{question_id}", response_model=QuestionInTestResponse, summary="Добавление существующего вопроса в тест")
async def add_existing_question_to_test(question: QuestionAddToTest, question_id: int, test_id: int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await question_service.add_existing_question_to_test(db, question, question_id, test_id, teacher_id)