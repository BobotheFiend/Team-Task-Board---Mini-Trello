from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemas.models.task import Task
from schemas.models.team_member import TeamMember


class Board(BaseModel):

    id: UUID | None = Field(default_factory=uuid4)
    tasks = [Task]
    owner_id = TeamMember.id
