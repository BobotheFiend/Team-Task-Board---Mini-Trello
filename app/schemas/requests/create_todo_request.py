from datetime import datetime, date, time

from pydantic import EmailStr, BaseModel
from app.schemas.models.enums.priority import Priority


class CreateTodoRequest(BaseModel):

    task_id: int
    current_user_id: int
    title: str
    assigned_to: int
    owner_email: EmailStr
    priority: Priority | None = None
    due_date: date
    due_time: time


