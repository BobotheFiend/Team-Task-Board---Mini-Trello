from datetime import date

from sqlmodel import SQLModel, Field

class UpdateTaskRequest(SQLModel):
    task_name: str
    update_due_date: date =  Field(..., description="Format: YYYY-MM-DD")
    team_name : str
    updated_by: str = Field(..., description="Enter Your Email")