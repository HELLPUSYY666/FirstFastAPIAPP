from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from database import Task


class TaskRepository:
    def __init__(self, db_session_maker: async_sessionmaker[AsyncSession]):
        self.db_session_maker = db_session_maker  # Теперь это async_sessionmaker, а не AsyncSession
        print(f"DEBUG: db_session_maker type = {type(self.db_session_maker)}")  # Проверка типа


    async def get_tasks(self, task_id: int = None) -> list[Task]:
        async with self.db_session_maker() as session:  # Вызываем фабрику, а не саму сессию
            if task_id:
                query = select(Task).where(Task.id == task_id)
            else:
                query = select(Task)
            result = await session.execute(query)
            return result.scalars().all()

    async def create_task(self, task: Task):
        async with self.db_session_maker() as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task

    async def delete_task(self, task_id: int):
        async with self.db_session_maker() as session:
            await session.execute(delete(Task).where(Task.id == task_id))
            await session.commit()

    async def update_task_name(self, task_id: int, name: str) -> Task:
        async with self.db_session_maker() as session:
            await session.execute(update(Task).where(Task.id == task_id).values(name=name))
            await session.commit()
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()

            if task is None:
                raise ValueError(f"Task with id {task_id} not found")

            return task
