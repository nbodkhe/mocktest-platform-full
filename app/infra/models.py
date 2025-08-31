from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255), default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Test(Base):
    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    mark_correct: Mapped[int] = mapped_column(Integer, default=1)
    mark_incorrect: Mapped[int] = mapped_column(Integer, default=0)
    subjects: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    subject: Mapped[str] = mapped_column(String(128))
    stem: Mapped[str] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSON)
    correct_index: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TestSession(Base):
    __tablename__ = "test_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    start_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active")
    client_fingerprint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    __table_args__ = (
        UniqueConstraint("test_id", "user_id", name="uq_session_test_user"),
    )


class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), index=True
    )
    chosen_index: Mapped[int] = mapped_column(Integer)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "test_id", "user_id", "question_id", name="uq_submission_user_test_question"
        ),
    )


class ScoreSnapshot(Base):
    __tablename__ = "score_snapshots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    total_score: Mapped[float] = mapped_column(Numeric(7, 2), default=0)
    subject_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    attempted: Mapped[int] = mapped_column(Integer, default=0)
    correct: Mapped[int] = mapped_column(Integer, default=0)
    incorrect: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("test_id", "user_id", name="uq_snapshot_user_test"),
    )


class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    rank: Mapped[int] = mapped_column(Integer)
    percentile: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    total_score: Mapped[float] = mapped_column(Numeric(7, 2), default=0)
    tiebreaker: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("test_id", "user_id", name="uq_lb_user_test"),)


class ScoreDistribution(Base):
    __tablename__ = "score_distributions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(
        ForeignKey("tests.id", ondelete="CASCADE"), index=True
    )
    subject: Mapped[str | None] = mapped_column(String(128), nullable=True)
    histogram: Mapped[dict] = mapped_column(JSON, default=dict)
    n: Mapped[int] = mapped_column(Integer, default=0)
    min: Mapped[float] = mapped_column(Numeric(7, 2), default=0)
    max: Mapped[float] = mapped_column(Numeric(7, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
