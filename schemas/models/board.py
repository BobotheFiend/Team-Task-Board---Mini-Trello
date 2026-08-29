from typing import Optional

from sqlmodel import SQLModel, Field, JSON

from schemas.models.task import Task
from schemas.models.todo import ToDo


class Board(SQLModel):

    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: list[Task] | None = Field(default=[], sa_type=JSON)
    completed_tasks: list[Task] | None = Field(default=[], sa_type=JSON)
    todos: list[ToDo] | None =  Field(default=[], sa_type=JSON)
    completed_todos: list[ToDo] | None = Field(default=[], sa_type=JSON)

