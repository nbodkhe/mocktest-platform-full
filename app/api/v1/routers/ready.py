from fastapi import APIRouter, HTTPException
from app.infra.redis import redis_client
from app.infra.db import engine
from sqlalchemy import text

router = APIRouter()

@router.get("/readyz")
async def readyz():
    try:
        pong = await redis_client.ping()
        if not pong:
            raise RuntimeError("redis not ready")
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
