from pydantic import BaseModel, Field, EmailStr


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str