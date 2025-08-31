"""auth fields

Revision ID: 0002_auth
Revises: 0001_init
Create Date: 2025-08-31
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_auth"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=False, server_default="")
    )
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false"))
    )
    op.execute("UPDATE users SET password_hash='' WHERE password_hash IS NULL")
    op.alter_column("users", "password_hash", server_default=None)


def downgrade():
    op.drop_column("users", "is_admin")
    op.drop_column("users", "password_hash")
