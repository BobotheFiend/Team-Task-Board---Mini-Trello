from app.exceptions.exception import TeamTaskBoardException


class TaskServiceException(TeamTaskBoardException):
    super.__init__("Task Service Exception")