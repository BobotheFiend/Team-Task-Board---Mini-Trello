from app.exceptions.exception import TeamTaskBoardException


class TodoServiceException(TeamTaskBoardException):
    def __init__(self, message: str):
        super().__init__(message)