# migrations/env.py

# --- Ensure our package is importable when Alembic runs ---
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# DO NOT call fileConfig(); our alembic.ini doesn't define logging sections
# from logging.config import fileConfig

import app.infra.models  # noqa: F401  # load models so tables exist in metadata

# Import app settings & metadata
from app.core.config import settings
from app.infra.db import Base  # ensures metadata

config = context.config

# Build a sync (psycopg2) URL for Alembic from our async one (asyncpg)
db_url = settings.DATABASE_URL
# Examples:
#   postgresql+asyncpg://...  -> postgresql+psycopg2://...
#   postgresql://...          -> postgresql+psycopg2://...
if "+asyncpg" in db_url:
    sync_url = db_url.replace("+asyncpg", "+psycopg2")
elif "postgresql://" in db_url and "+psycopg2" not in db_url:
    sync_url = db_url.replace("postgresql://", "postgresql+psycopg2://")
else:
    sync_url = db_url

# Tell Alembic what URL to use
config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
