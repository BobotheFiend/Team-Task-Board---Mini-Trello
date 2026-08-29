from enum import Enum

class Status(str, Enum):
    COMPLETED = "Completed"
    LATE = "Late"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"