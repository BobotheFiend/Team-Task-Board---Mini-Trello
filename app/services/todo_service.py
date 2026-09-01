from app.repositories.task_repository import TaskRepository
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.todo_repository import TodoRepository
from app.repositories.team_repository import TeamRepository

from app.schemas.models.todo import Todo
from app.schemas.requests.create_task_request import CreateTodoRequest


class TodoService:

    def __init__(
        self,
        todo_repository: TodoRepository,
        task_repository: TaskRepository,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository
    ):
        self.todo_repository = todo_repository
        self.task_repository = task_repository
        self.team_repository = team_repository
        self.team_member_repository = team_member_repository

    def create_todo(
        self,
        request: CreateTodoRequest,
        task_id: int,
        current_user_id: int
    ):

        current_user = self.team_member_repository.find_by_id(
            current_user_id
        )

        if current_user is None or not current_user.is_active:
            raise ValueError("User must be logged in")

        task = self.task_repository.find_by_id(task_id)

        if task is None:
            raise ValueError("Task not found")

        team = self.team_repository.find_by_id(task.team_id)

        if team is None:
            raise ValueError("Team not found")

        if team.lead != current_user_id:
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

        todo = Todo(
            title=request.title,
            assigned_to=request.assigned_to,
            priority=request.priority,
            due_date=request.due_date,
            task_id=task.id
        )

        return self.todo_repository.save(todo)


    def send_status_as_completed(self, request:):

