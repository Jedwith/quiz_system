from src.models import Test, question
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.question import Question
from src.models.question_test import QuestionTest
from src.schemas.question import QuestionCreateInTest, QuestionAddToTest, QuestionInTestResponse
from sqlalchemy import select
from fastapi import HTTPException, status

async def get_test_questions(db: AsyncSession, test_id: int, teacher_id:int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав доступа")

    result = await db.execute(
        select(Question, QuestionTest)
        .join(QuestionTest)
        .where(QuestionTest.test_id == test_id)
        .order_by(QuestionTest.order)
    )
    questions = [
        QuestionInTestResponse(
            id=question.id,
            text=question.text,
            type_id=question.type_id,
            order=link.order,
            points=link.points
        )
        for question, link in result.all()
    ]

    return questions

async def create_question_in_test(db: AsyncSession, question_data:QuestionCreateInTest, test_id:int, teacher_id:int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав доступа")

    question = Question(text=question_data.text, type_id=question_data.type_id)
    db.add(question)
    await db.flush()

    link = QuestionTest(
        test_id=test_id,
        question_id=question.id,
        order=question_data.order,
        points=question_data.points
    )
    db.add(link)
    await db.commit()
    await db.refresh(question)
    return QuestionInTestResponse(
        id=question.id,
        text=question.text,
        type_id=question.type_id,
        order=link.order,
        points=link.points
    )

async def add_existing_question_to_test(db: AsyncSession, question_data:QuestionAddToTest, question_id:int, test_id:int, teacher_id:int):
    result = await db.execute(select(Test).where(Test.id == test_id, Test.teacher_id == teacher_id))
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав доступа")

    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден или у вас нет прав доступа")

    result = await db.execute(select(QuestionTest).where(QuestionTest.test_id == test_id, QuestionTest.question_id == question_id))
    link = result.scalar_one_or_none()

    if link:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вопрос уже добавлен в тест")

    link = QuestionTest(
        test_id=test_id,
        question_id=question.id,
        order=question_data.order,
        points=question_data.points
    )
    db.add(link)
    await db.commit()
    await db.refresh(question)
    return QuestionInTestResponse(
        id=question.id,
        text=question.text,
        type_id=question.type_id,
        order=link.order,
        points=link.points
    )