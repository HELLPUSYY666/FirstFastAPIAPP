from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, status, Depends

from models import Task
from schema.task import TaskSchema
from repository import TaskRepository
from dependecy import get_task_repository, get_task_service
from service import TaskService

router = APIRouter(prefix='/task', tags=['tasks'])


@router.get('/all', response_model=list[TaskSchema])
async def get_task(task_service: Annotated[TaskService, Depends(get_task_service)]):
    tasks = await task_service.get_tasks()
    return [TaskSchema.model_validate(task) for task in tasks]


@router.post('/task', response_model=TaskSchema)
async def create_task(task: TaskSchema, task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    new_task = Task(
        name=task.name,
        pomodoro_count=task.pomodoro_count,
        category_id=task.category_id
    )

    created_task = await task_repository.create_task(new_task)

    return TaskSchema(
        id=created_task.id,
        name=created_task.name,
        pomodoro_count=created_task.pomodoro_count,
        category_id=created_task.category_id
    )


@router.patch('/{task_id}', response_model=TaskSchema)
async def update_task(task_id: int, name: str,
                      task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    try:
        updated_task = await task_repository.update_task_name(task_id, name)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Task {task_id} updated successfully"}


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    await task_repository.delete_task(task_id)
    return {"message": "Task deleted"}
