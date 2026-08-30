from pydantic import BaseModel, EmailStr


class LogoutUserRequest(BaseModel):
    email: EmailStr