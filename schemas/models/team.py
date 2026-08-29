from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field

from schemas.models.team_member import TeamMember


class Team(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., unique=True, index=True)
    members: list[TeamMember] = Field(default_factory=list)
    team_lead: TeamMember | None = None

