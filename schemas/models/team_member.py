
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr

from schemas.models.enums.role import Role


class TeamMember(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    email: EmailStr
    name: str
    password: str
    role: Role = Role.MEMBER
    is_active: bool | None = None

