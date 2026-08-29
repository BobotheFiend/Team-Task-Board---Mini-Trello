from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from schemas.models.enums.priority import Priority
from schemas.models.enums.status import Status

class ToDo(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    position: Optional[int] = None
    priority: Priority | None = Field(default_factory=Priority.MEDIUM)
    progress: Status = Status.PENDING
    due_date: datetime | None = None