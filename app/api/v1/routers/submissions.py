from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import json

from app.api.deps import get_session
from app.api.v1.schemas.submissions import SubmissionIn, SubmissionOut
from app.infra.models import Question, Submission
from app.domain.scoring import compute_score_update
from app.infra.redis import redis_client
from app.core.rate_limit import RateLimiter

router = APIRouter(prefix="/submit-answer")
limiter = RateLimiter(limit=120, window_seconds=60)

@router.post("", response_model=SubmissionOut, dependencies=[Depends(limiter)])
async def submit_answer(payload: SubmissionIn, session: AsyncSession = Depends(get_session), x_idempotency_key: str | None = Header(default=None)):
    if x_idempotency_key:
        cache_key = f"idem:submit:{x_idempotency_key}"
        cached = await redis_client.get(cache_key)
        if cached:
            d = json.loads(cached)
            return SubmissionOut(**d)

    res = await session.execute(select(Question).where(Question.id == payload.question_id, Question.test_id == payload.test_id))
    q = res.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = (payload.chosen_index == q.correct_index)
    stmt = insert(Submission).values(
        test_id=payload.test_id,
        user_id=payload.user_id,
        question_id=payload.question_id,
        chosen_index=payload.chosen_index,
        is_correct=is_correct,
        answered_at=datetime.utcnow()
    ).on_conflict_do_update(
        index_elements=["test_id","user_id","question_id"],
        set_={"chosen_index": payload.chosen_index, "is_correct": is_correct, "answered_at": datetime.utcnow()}
    )
    await session.execute(stmt)

    total, subject_scores, attempted, correct, incorrect = await compute_score_update(session, payload.test_id, payload.user_id)
    res_out = SubmissionOut(is_correct=is_correct, total_score=total, subject_scores=subject_scores)

    await session.commit()

    if x_idempotency_key:
        await redis_client.setex(cache_key, 86400, json.dumps(res_out.model_dump()))

    return res_out
