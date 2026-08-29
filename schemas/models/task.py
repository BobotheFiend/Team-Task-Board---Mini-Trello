from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, JSON

from schemas.models.team_member import TeamMember
from schemas.models.todo import ToDo


class Task(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    todos: list[int] | None = Field(default=[], sa_type=JSON)
    team_members : list[int] = Field(default=[], sa_type=JSON)
    due_date: datetime | None = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
