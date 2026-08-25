from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from priority import Priority
from status import Status

class ToDo(BaseModel):

    id: Optional[UUID] = Field(default_factory=uuid4);
    board_id: str | None = None
    description: str
    title: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    position: Optional[int]
    priority: Priority | None = None
    progress: Status = Status.IN_PROGRESS
    due_date: datetime | None = None