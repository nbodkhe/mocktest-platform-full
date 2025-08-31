import time
from fastapi import Request, HTTPException
from app.infra.redis import redis_client

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds

    async def __call__(self, request: Request):
        key = f"rl:{request.client.host}:{request.url.path}:{int(time.time()//self.window)}"
        n = await redis_client.incr(key)
        ttl = await redis_client.ttl(key)
        if ttl == -1:
            await redis_client.expire(key, self.window)
        if n > self.limit:
            raise HTTPException(status_code=429, detail="Too Many Requests")
