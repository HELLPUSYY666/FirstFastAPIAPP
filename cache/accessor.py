from typing import AsyncGenerator
import redis.asyncio as redis


async def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        password=None,
        decode_responses=True
    )


async def get_cache_session() -> AsyncGenerator[redis.Redis, None]:
    cache_session = await get_redis_connection()
    try:
        yield cache_session
    finally:
        await cache_session.close()


async def set_pomodoro_count():
    redis_conn = await get_redis_connection()
    await redis_conn.set('pomodoro_count', '1')
    await redis_conn.close()

