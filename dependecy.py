from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from cache import get_redis_connection
from database import get_session_maker
from repository import TaskRepository, TaskCacheRepository
from fastapi import Depends

from service import TaskService


async def get_task_repository(
        session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker)
) -> TaskRepository:
    return TaskRepository(session_maker)


async def get_task_cache_repository() -> TaskCacheRepository:
    redis_connection = await get_redis_connection()
    return TaskCacheRepository(redis_connection)


def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: TaskCacheRepository = Depends(get_task_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
