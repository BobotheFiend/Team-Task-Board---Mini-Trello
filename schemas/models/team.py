from typing import Optional

from sqlmodel import SQLModel, Field, JSON

from schemas.models.team_member import TeamMember


class Team(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...,unique=True, index=True)
    members: list[TeamMember] = Field(default=[], sa_type=JSON)
    team_lead: TeamMember | None = None

