from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from schemas.models.task import Task
from schemas.models.user import User


class Board(BaseModel):

    id: UUID | None = Field(default_factory=uuid4)
    tasks = [Task]
    owner_id = User.id
