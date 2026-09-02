from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.models.enums.status import Status


class CompletedStatusResponse(BaseModel):
    status: Status
    title: str
    timestamp: datetime = datetime.now()

    def __str__(self):
       return f"Your Request for {self.title} to be reviewed has been sent Successfully!\nDate: {self.timestamp}\nYour Progress Is Now: {self.status}"

