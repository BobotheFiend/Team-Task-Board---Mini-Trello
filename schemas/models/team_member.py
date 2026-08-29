
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from schemas.models.board import Board
from schemas.models.enums.role import Role


class TeamMember(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    name: str
    password: str
    role: Role = Field(default=Role.MEMBER)
    board_ID: Optional[int] = Field(default=None, foreign_key="board.ID")
    is_active: bool = Field(default=False)

