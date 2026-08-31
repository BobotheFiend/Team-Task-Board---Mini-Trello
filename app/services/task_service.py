from app.repositories.task_repository import TaskRepository
from app.repositories.team_repository import TeamRepository
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.todo_repository import TodoRepository
from app.schemas.requests.create_task_request import CreateTaskRequest
from app.schemas.models.task import Task


class TaskService:

    def __init__(
        self,
        task_repository: TaskRepository,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository,
        todo_repository: TodoRepository
    ):
        self.task_repository = task_repository
        self.team_repository = team_repository
        self.team_member_repository = team_member_repository
        self.todo_repository = todo_repository

    def create_task(
        self,
        request: CreateTaskRequest,
        current_user_id: int
    ):

        current_user = self.team_member_repository.find_by_id(
            current_user_id
        )

        if current_user is None or not current_user.is_active:
            raise ValueError("User must be logged in")

        team = self.team_repository.find_by_id(request.team_id)

        if team is None:
            raise ValueError("Team not found")

        if team.lead != current_user_id:
            raise ValueError("Only the team lead can create a task")

        existing_task = self.task_repository.find_by_task_title(
            request.title
        )

        if existing_task is not None:
            raise ValueError("Task with this title already exists")

        if request.todos is not None:

            for todo_request in request.todos:

                team_member = self.team_member_repository.find_by_id(
                    todo_request.assigned_to
                )

                if team_member is None:
                    raise ValueError(
                        f"Team member {todo_request.assigned_to} not found"
                    )

                if todo_request.assigned_to not in team.members_id:
                    raise ValueError(
                        f"Team member {todo_request.assigned_to} "
                        f"is not a member of this team"
                    )

        task = Task(
            title=request.title,
            team_id=request.team_id,
            due_date=request.due_date
        )

        saved_task = self.task_repository.save(task)

        return saved_task
