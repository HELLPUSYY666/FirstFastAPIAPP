from repository import TaskRepository, TaskCache
from database import get_db_session
from cache import get_redis_connection


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_task_cache_repository() -> TaskRepository:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)
