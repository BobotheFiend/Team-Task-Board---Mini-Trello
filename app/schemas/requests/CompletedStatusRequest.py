from pydantic import BaseModel

from app.schemas.models.enums.status import Status


class CompletedStatusRequest(BaseModel):

    status: Status = Status.PENDING
