from repository import TaskRepository, TaskCacheRepository
from schema.task import TaskSchema
from dataclasses import dataclass


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository

    async def get_tasks(self):
        tasks = await self.task_cache.get_all_tasks()
        if tasks:
            return tasks
        else:
            tasks = await self.task_repository.get_tasks()
            task_schema = [TaskSchema.model_validate(task) for task in tasks] if tasks else []
            await self.task_cache.set_tasks(task_schema)
            return task_schema
