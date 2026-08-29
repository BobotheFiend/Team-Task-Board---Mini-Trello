from typing import Optional

from sqlmodel import SQLModel, Field, JSON

from schemas.models.team_member import TeamMember


class Team(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...,unique=True, index=True, min_length=3, max_length=80)
    members_id: list[int] = Field(default=[], sa_type=JSON)
    lead: TeamMember | None = Field(default=None, sa_type=TeamMember)

