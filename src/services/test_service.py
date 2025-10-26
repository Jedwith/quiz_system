from src.models import Test
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from sqlalchemy import select
from src.schemas.test import TestCreate, TestUpdate
from fastapi import HTTPException, status

async def get_teacher_tests(db: AsyncSession, teacher_id: int):
    result = await db.execute(
        select(Test)
        .where(Test.teacher_id == teacher_id)
        .order_by(Test.created_at.desc())
    )
    tests = result.scalars().all()
    return tests

async def get_test_by_id(db: AsyncSession, test_id: int, teacher_id: int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав доступа")

    return test

async def create_test(db: AsyncSession, test_data:TestCreate, teacher_id: int):
    test = Test(
        name=test_data.name,
        description=test_data.description,
        teacher_id=teacher_id
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return test

async def update_test(db: AsyncSession, test_id:int, test_data:TestUpdate, teacher_id:int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав на ее редактирование")

    if test_data.name is not None:
        test.name = test_data.name
    if test_data.description is not None:
        test.description = test_data.description

    await db.commit()
    await db.refresh(test)
    return test

async def delete_test(db: AsyncSession, test_id:int, teacher_id:int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав на ее удаление")

    await db.delete(test)
    await db.commit()