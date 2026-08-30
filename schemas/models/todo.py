
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, JSON

from schemas.models.enums.priority import Priority
from schemas.models.enums.status import Status



class Todo(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(unique=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    position: Optional[int] = None
    assigned_to: int = Field(foreign_key="team_member.id")
    priority: Priority | None = Field(default=Priority.MEDIUM)
    progress: Status = Status.PENDING
    due_date: datetime | None = None
    task_id: int = Field(foreign_key="task.id")