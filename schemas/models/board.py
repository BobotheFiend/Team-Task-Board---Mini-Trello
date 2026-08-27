from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemas.models.task import Task
from schemas.models.todo import ToDo


class Board(BaseModel):

    id: UUID | None = Field(default_factory=uuid4)
    tasks: list[Task] | None = None
    completed_tasks: list[Task] | None = None
    todos: list[ToDo] | None = None
    completed_todos: list[ToDo] | None = None

