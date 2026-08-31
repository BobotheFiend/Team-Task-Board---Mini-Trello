from datetime import time, date

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, AutoString

from app.schemas.models.enums.priority import Priority


class CreateTodoRequest(SQLModel):

    todo_title: str
    todo_owner_email: EmailStr = Field(sa_type=AutoString)
    priority: Priority | None = None
    todo_due_date: date = Field(..., description="Format: YYYY-MM-DD")
    todo_due_time: time = Field(..., description="Format: HH:MM:SS")
    created_by: str = Field(..., description="Enter your Email")