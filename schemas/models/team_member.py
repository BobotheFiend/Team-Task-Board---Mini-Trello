
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from schemas.models.enums.role import Role


class TeamMember(SQLModel, table=True):
    __tablename__ = "team_member"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, sa_type=str)
    name: str
    password: str
    role: Role = Field(default=Role.MEMBER)
    board_id: Optional[int] = Field(default=None, foreign_key="board.id")
    is_active: bool = Field(default=False)

