from pydantic import BaseModel, Field, model_validator
from typing import Optional


class TaskSchema(BaseModel):
    id: Optional[int]
    name: str
    pomodoro_count: int | None = None
    category_id: int = Field(exclude=True)

    class Config:
        from_attributes = True

    @model_validator(mode='before')
    def check_name_not_none(self):
        if ['name'] is None:
            raise ValueError("Name cannot be None")
        else:
            return self
