
from typing import Optional

from pydantic import Field, EmailStr
from sqlalchemy import true
from sqlmodel import SQLModel

from schemas.models.board import Board
from schemas.models.enums.role import Role


class TeamMember(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    name: str
    password: str
    role: Role = Role.MEMBER
    board: Board = Board()
    is_active: bool = False

