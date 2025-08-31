from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_session
from app.infra.models import Leaderboard
from app.core.rate_limit import RateLimiter

router = APIRouter(prefix="/leaderboard")
limiter = RateLimiter(limit=300, window_seconds=60)

@router.get("/{test_id}", dependencies=[Depends(limiter)])
async def leaderboard(test_id: int, page: int = 1, size: int = 20, session: AsyncSession = Depends(get_session)):
    offset = (page - 1) * size
    res = await session.execute(select(Leaderboard).where(Leaderboard.test_id == test_id).order_by(Leaderboard.rank.asc()).offset(offset).limit(size))
    rows = res.scalars().all()
    return [{"user_id": r.user_id, "rank": r.rank, "percentile": float(r.percentile), "total_score": float(r.total_score)} for r in rows]
