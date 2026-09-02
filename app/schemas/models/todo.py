
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, JSON, AutoString

from app.schemas.models.enums.priority import Priority
from app.schemas.models.enums.status import Status



class Todo(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(unique=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    position: Optional[int] = None
    assigned_to: int = Field(foreign_key="team_member.id")
    owner_email: EmailStr = Field(sa_type=AutoString)
    priority: Priority | None = Field(default=Priority.MEDIUM)
    progress: Status = Status.IN_PROGRESS
    due: datetime | None = None
    task_id: int = Field(foreign_key="task.id")