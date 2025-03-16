from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import Task, get_db_session, Category
from schema.task import TaskSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int):
        query = select(Task).where(Task.id == task_id)
        with self.db_session() as session:
            task = session.execute(query).scalars().all()
        return task

    def get_tasks(self, task_id: int = None) -> list[Task]:
        with self.db_session() as session:
            if task_id:
                tasks = session.execute(select(Task).where(Task.id == task_id)).scalars().all()
            else:
                tasks = session.execute(select(Task)).scalars().all()
        return tasks

    def create_task(self, task: Task):
        with self.db_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def delete_task(self, task_id: int):
        with self.db_session() as session:
            session.execute(delete(Task).where(Task.id == task_id))
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Task]:
        query = select(Task).join(Category, Task.category_id == Category.id).where(Task.category_id == category_name)
        with self.db_session() as session:
            task = list[Task] = session.execute(query).scalars().all()
            return task

