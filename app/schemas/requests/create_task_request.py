from datetime import date

from sqlmodel import SQLModel, Field

from app.schemas.models.team import Team


class CreateTaskRequest(SQLModel):
    team_name: str
    team_members_email: list[str]
    task_due_date: date =  Field(..., description="Format: YYYY-MM-DD")
    task_name : str = Field(..., description="Name of the task")
    created_by: str = Field(..., description="Enter Your Email")