from datetime import datetime

from pydantic import BaseModel

from app.schemas.models.enums.priority import Priority


class CreateTodoRequest(BaseModel):
    title: str
    assigned_to: int
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None


class CreateTaskRequest(BaseModel):
    title: str
    team_id: int
    due_date: datetime | None = None
    todos: list[CreateTodoRequest] | None = None

