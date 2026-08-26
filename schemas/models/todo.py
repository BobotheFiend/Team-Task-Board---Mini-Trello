from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from schemas.models.enums.priority import Priority
from schemas.models.enums.status import Status

class ToDo(BaseModel):

    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    position: Optional[int] = None
    priority: Priority | None = None
    progress: Status = Status.PENDING
    due_date: datetime | None = None