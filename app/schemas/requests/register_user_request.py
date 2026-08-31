from pydantic import BaseModel, EmailStr, Field

from app.schemas.models.enums.role import Role


class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8,max_length=20)
    role: Role
