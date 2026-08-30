
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, AutoString

from app.schemas.models.enums.role import Role


class TeamMember(SQLModel, table=True):
    __tablename__ = "team_member"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    name: str
    password: str = Field(validation_alias="######")
    role: Role = Field(default=Role.MEMBER)
    is_active: bool = Field(default=False)

