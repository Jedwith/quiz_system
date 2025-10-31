from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Answer, Question, Test, QuestionTest
from src.schemas.answer import AnswerCreate, AnswerUpdate, AnswerResponse
from sqlalchemy import select, func
from fastapi import HTTPException, status

async def get_answers_by_question(db: AsyncSession, question_id: int, teacher_id: int):
    result = await db.execute(
        select(Question)
        .join(QuestionTest, Question.id == QuestionTest.question_id)
        .join(Test, QuestionTest.test_id == Test.id)
        .where(Question.id == question_id, Test.teacher_id == teacher_id)
        .limit(1)
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден или у вас нет прав доступа"
        )

    result = await db.execute(
        select(Answer)
        .where(Answer.question_id == question_id)
        .order_by(Answer.order)
    )
    answers = result.scalars().all()

    return answers

async def create_answer(db: AsyncSession, question_id: int, answer_data: AnswerCreate, teacher_id: int):
    result = await db.execute(
        select(Question)
        .join(QuestionTest, Question.id == QuestionTest.question_id)
        .join(Test, QuestionTest.test_id == Test.id)
        .where(Question.id == question_id, Test.teacher_id == teacher_id)
        .limit(1)
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден или у вас нет прав доступа"
        )

    # Автоматический order
    count_result = await db.execute(
        select(func.count(Answer.id)).where(Answer.question_id == question_id)
    )
    current_count = count_result.scalar_one()
    new_order = current_count + 1

    answer = Answer(
        text=answer_data.text,
        is_correct=answer_data.is_correct,
        order=new_order,
        question_id=question_id
    )
    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer

async def update_answer(db: AsyncSession, answer_id: int, answer_data: AnswerUpdate, teacher_id: int):
    result = await db.execute(
        select(Answer)
        .join(Question, Answer.question_id == Question.id)
        .join(QuestionTest, Question.id == QuestionTest.question_id)
        .join(Test, QuestionTest.test_id == Test.id)
        .where(Answer.id == answer_id, Test.teacher_id == teacher_id)
        .limit(1)
    )
    answer = result.scalar_one_or_none()

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вариант ответа не найден или у вас нет прав доступа"
        )
    if answer_data.text is not None:
        answer.text = answer_data.text
    if answer_data.is_correct is not None:
        answer.is_correct = answer_data.is_correct

    await db.commit()
    await db.refresh(answer)
    return answer

async def delete_answer(db: AsyncSession, answer_id: int, teacher_id: int):
    result = await db.execute(
        select(Answer)
        .join(Question, Answer.question_id == Question.id)
        .join(QuestionTest, Question.id == QuestionTest.question_id)
        .join(Test, QuestionTest.test_id == Test.id)
        .where(Answer.id == answer_id, Test.teacher_id == teacher_id)
        .limit(1)
    )
    answer = result.scalar_one_or_none()

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вариант ответа не найден или у вас нет прав доступа"
        )

    await db.delete(answer)
    await db.commit()



