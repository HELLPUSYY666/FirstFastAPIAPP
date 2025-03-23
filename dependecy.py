from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import Depends, Request, security, Security, HTTPException

from cache import get_redis_connection
from database import get_session_maker
from exception import TokenExpiredException, TokenNotCorrectException
from repository import TaskRepository, TaskCacheRepository, UserRepository
from service import TaskService, UserService, AuthService


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


def get_user_repository(
        session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker)
) -> UserRepository:
    return UserRepository(session_maker)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id

