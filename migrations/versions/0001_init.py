"""initial schema

Revision ID: 0001_init
Revises:
Create Date: 2025-08-31
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    # tests
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("mark_correct", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("mark_incorrect", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("subjects", sa.JSON(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # questions
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", sa.String(length=128), nullable=False),
        sa.Column("stem", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_index", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_questions_test_id", "questions", ["test_id"])

    # test_sessions
    op.create_table(
        "test_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("end_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("client_fingerprint", sa.String(length=255), nullable=True),
        sa.Column("ip", sa.String(length=64), nullable=True),
        sa.UniqueConstraint("test_id", "user_id", name="uq_session_test_user"),
    )
    op.create_index("ix_test_sessions_test_id", "test_sessions", ["test_id"])
    op.create_index("ix_test_sessions_user_id", "test_sessions", ["user_id"])

    # submissions
    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chosen_index", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("answered_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("test_id", "user_id", "question_id", name="uq_submission_user_test_question"),
    )
    op.create_index("ix_submissions_test_id", "submissions", ["test_id"])
    op.create_index("ix_submissions_user_id", "submissions", ["user_id"])
    op.create_index("ix_submissions_question_id", "submissions", ["question_id"])

    # score_snapshots
    op.create_table(
        "score_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_score", sa.Numeric(7, 2), nullable=False, server_default="0"),
        sa.Column("subject_scores", sa.JSON(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("attempted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("incorrect", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_updated", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("test_id", "user_id", name="uq_snapshot_user_test"),
    )
    op.create_index("ix_score_snapshots_test_id", "score_snapshots", ["test_id"])
    op.create_index("ix_score_snapshots_user_id", "score_snapshots", ["user_id"])

    # leaderboard
    op.create_table(
        "leaderboard",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("percentile", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("total_score", sa.Numeric(7, 2), nullable=False, server_default="0"),
        sa.Column("tiebreaker", sa.JSON(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.UniqueConstraint("test_id", "user_id", name="uq_lb_user_test"),
    )
    op.create_index("ix_leaderboard_test_id", "leaderboard", ["test_id"])
    op.create_index("ix_leaderboard_user_id", "leaderboard", ["user_id"])

    # score_distributions
    op.create_table(
        "score_distributions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("test_id", sa.Integer(), sa.ForeignKey("tests.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", sa.String(length=128), nullable=True),
        sa.Column("histogram", sa.JSON(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("n", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min", sa.Numeric(7, 2), nullable=False, server_default="0"),
        sa.Column("max", sa.Numeric(7, 2), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_score_distributions_test_id", "score_distributions", ["test_id"])


def downgrade():
    op.drop_table("score_distributions")
    op.drop_table("leaderboard")
    op.drop_table("score_snapshots")
    op.drop_table("submissions")
    op.drop_table("test_sessions")
    op.drop_table("questions")
    op.drop_table("tests")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
