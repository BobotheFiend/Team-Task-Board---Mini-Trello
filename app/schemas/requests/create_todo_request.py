from datetime import datetime
from sqlmodel import SQLModel
from app.schemas.models.enums.priority import Priority


class CreateTodoRequest(SQLModel):

    title: str
    assigned_to: int
    priority: Priority | None = None
    due_date: datetime | None = None

