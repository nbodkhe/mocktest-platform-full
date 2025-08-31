import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.leaderboard import router as leaderboard_router
from app.api.v1.routers.predict import router as predict_router
from app.api.v1.routers.questions import router as questions_router
from app.api.v1.routers.ready import router as ready_router
from app.api.v1.routers.results import router as results_router
from app.api.v1.routers.sessions import router as sessions_router
from app.api.v1.routers.submissions import router as submissions_router
from app.api.v1.routers.tests import router as tests_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.infra.db import engine
from app.infra.redis import redis_client


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = rid
        start = time.time()
        response = await call_next(request)
        latency_ms = round((time.time() - start) * 1000, 2)
        response.headers["x-request-id"] = rid
        logger.bind(
            request_id=rid,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            latency_ms=latency_ms,
        ).info("HTTP")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # (no middleware/Instrumentator setup here — app has already started at this point)
    yield
    try:
        await redis_client.close()
    except Exception:
        pass
    try:
        await engine.dispose()
    except Exception:
        pass


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

    # Middlewares must be added before the app starts
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(RequestIDMiddleware)

    # Routers
    app.include_router(health_router, prefix=settings.API_V1_PREFIX, tags=["health"])
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX, tags=["auth"])
    app.include_router(tests_router, prefix=settings.API_V1_PREFIX, tags=["tests"])
    app.include_router(
        questions_router, prefix=settings.API_V1_PREFIX, tags=["questions"]
    )
    app.include_router(
        sessions_router, prefix=settings.API_V1_PREFIX, tags=["sessions"]
    )
    app.include_router(
        submissions_router, prefix=settings.API_V1_PREFIX, tags=["submissions"]
    )
    app.include_router(results_router, prefix=settings.API_V1_PREFIX, tags=["results"])
    app.include_router(
        leaderboard_router, prefix=settings.API_V1_PREFIX, tags=["leaderboard"]
    )
    app.include_router(predict_router, prefix=settings.API_V1_PREFIX, tags=["predict"])
    app.include_router(ready_router, tags=["health"])  # /readyz

    # Prometheus instrumentation must be configured at import time / before startup
    Instrumentator().instrument(app).expose(
        app, endpoint="/metrics", include_in_schema=False
    )

    return app


app = create_app()
