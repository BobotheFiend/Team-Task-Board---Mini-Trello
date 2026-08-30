from pydantic import BaseModel, Field, EmailStr


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)