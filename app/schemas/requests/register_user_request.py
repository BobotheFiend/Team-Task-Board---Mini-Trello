from pydantic import BaseModel, EmailStr, Field

from schemas.models.enums.role import Role


class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., le=8,ge=20)
    role: Role
