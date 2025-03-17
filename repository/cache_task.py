from redis import Redis

from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self):
        pass

    def set_tasks(self, tasks: list[TaskSchema]):
        task_json = [task.json() for task in tasks]

        self.redis.lpush('tasks', *task_json)
