from app.exceptions.exception import TeamTaskBoardException


class TaskServiceException(TeamTaskBoardException):
    def __init__(self, message: str):
        super().__init__(message)