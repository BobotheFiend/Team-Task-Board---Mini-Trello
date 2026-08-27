from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemas.models.team_member import TeamMember
from schemas.models.todo import ToDo


class Task(BaseModel):

    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str
    todos: list[ToDo] | None = None
    team_members : list[TeamMember]
    due_date: datetime | None = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
