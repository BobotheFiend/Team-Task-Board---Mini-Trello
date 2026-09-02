from datetime import datetime

from pydantic import BaseModel

from app.schemas.requests.create_todo_request import CreateTodoRequest


class CreateTaskRequest(BaseModel):
    title: str
    team_id: int
    due_date: datetime | None = None
    todos: list[CreateTodoRequest] | None = None

