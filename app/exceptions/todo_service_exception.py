from app.exceptions.exception import TeamTaskBoardException


class TodoServiceException(TeamTaskBoardException):
    super.__init__("Todo Service Exception")