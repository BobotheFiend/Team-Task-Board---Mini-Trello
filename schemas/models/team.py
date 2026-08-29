from typing import Optional

from sqlmodel import SQLModel, Field, JSON



class Team(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...,unique=True, index=True, min_length=3, max_length=80)
    members_id: list[int] = Field(default=[], sa_type=JSON)
    lead: int | None = Field(default=None, foreign_key="team_member.id")

