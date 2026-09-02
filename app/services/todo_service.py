from datetime import datetime

from app.exceptions.todo_service_exception import TodoServiceException
from app.repositories.task_repository import TaskRepository
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.todo_repository import TodoRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.models.enums.status import Status

from app.schemas.models.todo import Todo
from app.schemas.requests.completed_status_request import CompletedStatusRequest
from app.schemas.requests.create_task_request import CreateTodoRequest
from app.schemas.responses.completed_status_response import CompletedStatusResponse


class TodoService:

    def __init__(
        self,
        todo_service_repository: TodoRepository,
        task_repository: TaskRepository,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository
    ):
        self.todo_repository = todo_service_repository
        self.task_repository = task_repository
        self.team_repository = team_repository
        self.team_member_repository = team_member_repository

    def create_todo(self, request: CreateTodoRequest):

        current_user = self.team_member_repository.find_by_id(request.current_user_id)

        if current_user is None or not current_user.is_active:
            raise ValueError("User must be logged in")

        task = self.task_repository.find_by_id(request.task_id)

        if task is None:
            raise ValueError("Task not found")

        team = self.team_repository.find_by_id(task.team_id)

        if team is None:
            raise ValueError("Team not found")

        if team.lead != request.current_user_id:
            raise ValueError(
                "Only the team lead can create a todo"
            )

        assigned_member = self.team_member_repository.find_by_id(
            request.assigned_to
        )

        if assigned_member is None:
            raise ValueError(
                f"Team member {request.assigned_to} not found"
            )

        if request.assigned_to not in team.members_id:
            raise ValueError(
                f"Team member {request.assigned_to} "
                f"is not a member of this team"
            )

        due_date_time = datetime.combine(request.due_date, request.due_time)

        todo = Todo(
            title=request.title,
            created_at=datetime.now(),
            assigned_to=request.assigned_to,
            priority=request.priority,
            task_id=task.id,
            owner_email=current_user.email,
            due=due_date_time
        )

        return self.todo_repository.save(todo)


    def send_status_as_completed(self, request:CompletedStatusRequest) -> CompletedStatusResponse | str:
        found_user = self.team_member_repository.find_by_email(request.member_email)
        if found_user is None:
            raise TodoServiceException("User not found !")

        if not found_user.is_active:
            raise TodoServiceException("User Is Not Logged In !")


        found_todo = self.todo_repository.find_by_todo_title(request.todo_title)
        if found_todo is None:
            raise TodoServiceException("Todo Does Not Exist")
        if found_todo.progress == Status.LATE:
            raise TodoServiceException("Todo is Already Late!")
        if found_todo.progress == Status.COMPLETED:
            raise TodoServiceException("Todo Already Completed")
        if found_todo.progress == Status.PENDING:
            raise TodoServiceException("Todo UnderGoing Review!")

        found_todo.progress = Status.PENDING

        self.todo_repository.save(found_todo)

        response = CompletedStatusResponse(title=found_todo.title, status=found_todo.progress)
        response.message = f"Your Request for {response.title} to be reviewed has been sent Successfully!\nDate: {response.timestamp}\nYour Progress Is Now: {response.status}"
        return response

