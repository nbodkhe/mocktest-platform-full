from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "mocktest-platform"
    ENV: str = "local"
    API_V1_PREFIX: str = "/api/v1"

    # Auth
    SECRET_KEY: str = "dev"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # Data stores
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/mocktest"
    REDIS_URL: str = "redis://redis:6379/0"
    BROKER_URL: str = "redis://redis:6379/1"
    RESULT_BACKEND: str = "redis://redis:6379/2"

    # Runtime
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000
    WORKERS: int = 2

    class Config:
        env_file = ".env"


settings = Settings()
