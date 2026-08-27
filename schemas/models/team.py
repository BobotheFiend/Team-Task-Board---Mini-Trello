from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from schemas.models.team_member import TeamMember


class Team(BaseModel):

    _id : Optional[str] = Field(default_factory=uuid4)
    _members: list[TeamMember] = Field(default_factory=list)
    _team_lead: TeamMember | None = None

