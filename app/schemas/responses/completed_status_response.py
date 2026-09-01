from datetime import datetime

from pydantic import BaseModel

from app.schemas.models.enums.status import Status


class CompletedStatusResponse(BaseModel):
    status: Status
    title: str
    timestamp: datetime = datetime.now()
    message: str

    __str__ =  f"{message}"

