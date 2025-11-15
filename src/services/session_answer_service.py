from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Test, Question, QuestionTest, Room, TestSession, SessionAnswer, Answer
from src.schemas.session_answer import SessionAnswerCreate, SessionAnswerResponse
from sqlalchemy import select
from fastapi import HTTPException, status

async def save_student_answer(db: AsyncSession, session_answer_data: SessionAnswerCreate, session_id: int, student_id: int):
    result = await db.execute(select(TestSession).where(TestSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не найдена"
        )

    if session.end_time is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Сессия уже завершена"
        )

    result = await db.execute(select(Question).where(Question.id == session_answer_data.question_id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не найден"
        )

    result = await db.execute(
        select(QuestionTest)
        .where(QuestionTest.test_id == session.test_id, QuestionTest.question_id == session_answer_data.question_id)
    )
    question_link = result.scalar_one_or_none()

    if not question_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вопрос не пренадлежит тесту этой сессии"
        )

    result = await db.execute(
        select(SessionAnswer)
        .where(
            SessionAnswer.session_id == session_id,
            SessionAnswer.question_id == session_answer_data.question_id,
            # SessionAnswer.answer_id == session_answer_data.answer_id,
            SessionAnswer.student_id == student_id
        )
    )

    existing_answer = result.scalar_one_or_none()

    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="На этот вопрос уже был дан ответ"
        )

    answered_at = datetime.now(timezone.utc)
    is_correct = False
    new_answer = None

    # Один вариант ответа
    if question.type_id == 1:
        if not session_answer_data.answer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо выбрать вариант ответа"
            )

        answer = await db.get(Answer, session_answer_data.answer_id)

        if not answer or answer.question_id != session_answer_data.question_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вариант ответа не найден или не принадлежит этому вопросу"
            )
        is_correct = answer.is_correct

        new_answer = SessionAnswer(
            session_id=session_id,
            student_id=student_id,
            question_id=session_answer_data.question_id,
            answer_id=session_answer_data.answer_id,
            is_correct=is_correct,
            answered_at=answered_at
        )
        db.add(new_answer)

    elif question.type_id == 2:
        selected_ids = session_answer_data.answer_ids
        if not selected_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо выбрать хотя бы один вариант ответа"
            )

        result = await db.execute(
            select(Answer)
            .where(Answer.id.in_(selected_ids))
        )
        answers = result.scalars().all()

        if len(answers) != len(selected_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Некоторые варианты ответа не найдены"
            )

        if any(a.question_id != session_answer_data.question_id for a in answers):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Варианты ответа не принадлежат вопросу"
            )

        result = await db.execute(
            select(Answer.id)
            .where(
                Answer.question_id == session_answer_data.question_id,
                Answer.is_correct == True
            )
        )

        correct_ids = set(result.scalars().all())
        is_correct = set(selected_ids) == correct_ids

        for answer_id in selected_ids:
            ans = SessionAnswer(
                session_id=session_id,
                student_id=student_id,
                question_id=session_answer_data.question_id,
                answer_id=answer_id,
                is_correct=(answer_id in correct_ids),
                answered_at=answered_at
            )
            db.add(ans)
            if new_answer is None:
                new_answer = ans

    elif question.type_id == 3:
        if not session_answer_data.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо ввести текст ответа"
            )

        cleaned_text = session_answer_data.text.strip().lower()

        result = await db.execute(
            select(Answer.text)
            .where(
                Answer.question_id == session_answer_data.question_id,
                Answer.is_correct == True
            )
        )

        correct_texts = {t.strip().lower() for t in result.scalars().all()}

        is_correct = cleaned_text in correct_texts

        new_answer = SessionAnswer(
            session_id=session_id,
            student_id=student_id,
            question_id=session_answer_data.question_id,
            text=session_answer_data.text,
            is_correct=is_correct,
            answered_at=answered_at
        )
        db.add(new_answer)

    await db.commit()
    await db.refresh(new_answer)

    return SessionAnswerResponse(
        id=new_answer.id,
        session_id=session_id,
        student_id=student_id,
        question_id=session_answer_data.question_id,
        answer_id=session_answer_data.answer_id if question.type_id == 1 else None,
        answer_ids=session_answer_data.answer_ids if question.type_id == 2 else None,
        text=session_answer_data.text if question.type_id == 3 else None,
        is_correct=is_correct,
        answered_at=answered_at
    )



