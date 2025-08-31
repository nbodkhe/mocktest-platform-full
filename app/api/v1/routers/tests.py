from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.v1.routers.auth import get_current_admin  # <-- guard
from app.api.v1.schemas.tests import TestCreate, TestOut
from app.infra.models import Test

router = APIRouter(prefix="/tests")


@router.post(
    "",
    response_model=TestOut,
    status_code=201,
    dependencies=[Depends(get_current_admin)],
)
async def create_test(
    payload: TestCreate, session: AsyncSession = Depends(get_session)
):
    t = Test(
        name=payload.name,
        duration_minutes=payload.duration_minutes,
        mark_correct=payload.mark_correct,
        mark_incorrect=payload.mark_incorrect,
        subjects=payload.subjects,
        status="live",
    )
    session.add(t)
    await session.commit()
    await session.refresh(t)
    return TestOut(
        id=t.id,
        name=t.name,
        duration_minutes=t.duration_minutes,
        mark_correct=t.mark_correct,
        mark_incorrect=t.mark_incorrect,
        subjects=t.subjects,
        status=t.status,
    )


@router.get("", response_model=list[TestOut])
async def list_tests(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Test))
    rows = res.scalars().all()
    return [
        TestOut(
            id=x.id,
            name=x.name,
            duration_minutes=x.duration_minutes,
            mark_correct=x.mark_correct,
            mark_incorrect=x.mark_incorrect,
            subjects=x.subjects,
            status=x.status,
        )
        for x in rows
    ]
