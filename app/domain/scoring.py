from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from sqlalchemy.dialects.postgresql import insert
from app.infra.models import Submission, ScoreSnapshot, Question, Test

async def compute_score_update(session: AsyncSession, test_id: int, user_id: int):
    t = (await session.execute(select(Test).where(Test.id == test_id))).scalar_one()
    mark_c = t.mark_correct
    mark_i = t.mark_incorrect

    res = await session.execute(select(Submission.question_id, Submission.is_correct).where(Submission.test_id == test_id, Submission.user_id == user_id))
    rows = res.fetchall()
    correct = sum(1 for _, is_c in rows if is_c)
    attempted = len(rows)
    incorrect = attempted - correct
    total = correct * mark_c + incorrect * mark_i

    sq = select(
        Question.subject,
        func.sum(case((Submission.is_correct == True, mark_c), else_=mark_i))
    ).join(Submission, Submission.question_id == Question.id)\
     .where(Submission.test_id == test_id, Submission.user_id == user_id)\
     .group_by(Question.subject)
    res2 = await session.execute(sq)
    subject_scores = {subject: float(score) for subject, score in res2.all()}

    upsert = insert(ScoreSnapshot).values(
        test_id=test_id, user_id=user_id, total_score=total, subject_scores=subject_scores,
        attempted=attempted, correct=correct, incorrect=incorrect
    ).on_conflict_do_update(
        index_elements=["test_id","user_id"],
        set_={"total_score": total, "subject_scores": subject_scores, "attempted": attempted, "correct": correct, "incorrect": incorrect}
    )
    await session.execute(upsert)
    return float(total), subject_scores, attempted, correct, incorrect
