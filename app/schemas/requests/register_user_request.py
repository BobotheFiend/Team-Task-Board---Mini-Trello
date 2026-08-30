import sqlmodel
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class RegisterUserRequest(SQLModel):
    name: str
    email: EmailStr
    password: str = Field(..., max_length=20,min_length=8)
