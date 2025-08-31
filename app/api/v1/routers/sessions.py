from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.api.deps import get_session
from app.api.v1.schemas.sessions import SessionCreate, SessionOut
from app.infra.models import Test, TestSession

router = APIRouter(prefix="/sessions")

@router.post("", response_model=SessionOut, status_code=201)
async def start_session(payload: SessionCreate, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Test).where(Test.id == payload.test_id))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Test not found")
    s = TestSession(test_id=payload.test_id, user_id=payload.user_id, start_at=datetime.utcnow(), end_at=datetime.utcnow() + timedelta(minutes=t.duration_minutes), status="active")
    session.add(s)
    await session.commit()
    await session.refresh(s)
    return SessionOut(id=s.id, test_id=s.test_id, user_id=s.user_id, start_at=s.start_at, end_at=s.end_at, status=s.status)
