from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, JSON, AutoString


class Team(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...,unique=True, index=True, min_length=3, max_length=80)
    members_id: list[int] = Field(default=[], sa_type=JSON)
    members_email: list[EmailStr] | None = Field(default=None, sa_type=JSON)
    lead: int | None = Field(default=None, foreign_key="team_member.id")

