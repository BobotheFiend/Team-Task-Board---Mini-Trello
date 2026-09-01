from pydantic import BaseModel

from app.schemas.models.enums.status import Status


class CompletedStatusRequest(BaseModel):
    todo_title: str
    status: Status = Status.PENDING
