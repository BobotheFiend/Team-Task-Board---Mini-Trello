from typing import Optional

from sqlmodel import SQLModel, Field, JSON


class Board(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    task_ids: list[int] | None = Field(default=[], sa_type=JSON)
    todo_ids: list[int] | None = Field(default=[], sa_type=JSON)


