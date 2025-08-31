from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_session
from app.infra.models import ScoreSnapshot

router = APIRouter(prefix="/results")

@router.get("/my/{test_id}")
async def my_result(test_id: int, user_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(ScoreSnapshot).where(ScoreSnapshot.test_id == test_id, ScoreSnapshot.user_id == user_id))
    row = res.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return {"test_id": test_id, "user_id": user_id, "total_score": float(row.total_score), "subject_scores": row.subject_scores, "attempted": row.attempted, "correct": row.correct, "incorrect": row.incorrect}
