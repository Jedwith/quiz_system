from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.test import TestCreate, TestUpdate, TestResponse
from src.services import test_service
from src.core.dependencies import get_teacher_id

router = APIRouter(prefix="/tests", tags=["Tests"])

@router.get("/", response_model=List[TestResponse], summary="Получение тестов преподавателя")
async def get_tests(teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_service.get_teacher_tests(db, teacher_id)

@router.get("/{test_id}", response_model=TestResponse, summary="Получение теста по ID")
async def get_test_by_id(test_id:int, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_service.get_test_by_id(db, test_id, teacher_id)

@router.post("/", response_model=TestResponse, summary="Создание теста")
async def create_test(test: TestCreate, teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_service.create_test(db, test, teacher_id)

@router.patch("/{test_id}", response_model=TestResponse, summary="Редактирование теста")
async def update_test(test: TestUpdate, test_id: int = Path(..., gt=0), teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_service.update_test(db, test_id, test, teacher_id)

@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление теста")
async def delete_test(test_id: int = Path(..., gt=0), teacher_id: int = Depends(get_teacher_id), db: AsyncSession = Depends(get_db)):
    return await test_service.delete_test(db, test_id, teacher_id)

