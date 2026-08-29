from typing import Optional

from sqlmodel import SQLModel, Field, JSON

from schemas.models.task import Task
from schemas.models.todo import ToDo


class Board(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    member_ID: int = Field(foreign_key='teammember.ID')


