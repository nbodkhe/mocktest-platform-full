from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.v1.routers.auth import get_current_admin  # <-- guard
from app.api.v1.schemas.questions import QuestionCreate, QuestionOut
from app.infra.models import Question

router = APIRouter(prefix="/questions")


@router.post(
    "",
    response_model=QuestionOut,
    status_code=201,
    dependencies=[Depends(get_current_admin)],
)
async def create_question(
    payload: QuestionCreate, session: AsyncSession = Depends(get_session)
):
    q = Question(
        test_id=payload.test_id,
        subject=payload.subject,
        stem=payload.stem,
        options=payload.options,
        correct_index=payload.correct_index,
        difficulty=payload.difficulty,
    )
    session.add(q)
    await session.commit()
    await session.refresh(q)
    return QuestionOut(
        id=q.id,
        test_id=q.test_id,
        subject=q.subject,
        stem=q.stem,
        options=q.options,
        correct_index=q.correct_index,
        difficulty=q.difficulty,
    )
