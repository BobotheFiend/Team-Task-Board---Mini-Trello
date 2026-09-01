from pydantic import BaseModel

from app.schemas.models.enums.status import Status


class CompletedStatusRequest(BaseModel):
    todo_title: str
    set_current_status: Status = Status.PENDING
