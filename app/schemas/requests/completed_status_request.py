from pydantic import BaseModel, Field, EmailStr

from app.schemas.models.enums.status import Status


class CompletedStatusRequest(BaseModel):
    todo_title: str
    member_email: EmailStr
