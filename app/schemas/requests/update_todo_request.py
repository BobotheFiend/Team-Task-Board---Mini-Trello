from datetime import date, time

from pydantic import EmailStr
from sqlmodel import SQLModel, AutoString, Field

from schemas.models.enums.priority import Priority


class CreateTodoRequest(SQLModel):

    todo_title: str
    todo_owner_email: EmailStr = Field(sa_type=AutoString)
    update_priority: Priority | None = None
    update_todo_due_date: date = Field(..., description="Format: YYYY-MM-DD")
    update_todo_due_time: time = Field(..., description="Format: HH:MM:SS")
    updated_by: str = Field(..., description="Enter your Email")