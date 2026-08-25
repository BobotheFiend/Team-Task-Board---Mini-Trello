from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4);
    email: EmailStr;
    name: str;
    password: str;
    is_active: bool | None = None;

