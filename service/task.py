from repository import TaskRepository, TaskCacheRepository
from schema.task import TaskSchema, TaskCreateSchema
from dataclasses import dataclass


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository

    async def get_tasks(self) -> list[TaskSchema]:
        tasks = await self.task_cache.get_all_tasks()

        if tasks:
            return tasks

        tasks = await self.task_repository.get_tasks()

        if tasks:
            task_schema = [TaskSchema.model_validate(task.__dict__) for task in tasks]
            await self.task_cache.set_all_tasks(task_schema)
            return task_schema
        else:
            return []

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task = await self.task_repository.create_task(body, user_id)
        return TaskSchema.model_validate(task.__dict__)
