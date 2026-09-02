import datetime


import pytest
from sqlmodel import Session

from app.repositories.task_repository import TaskRepository
from app.repositories.task_repository_impl import TaskRepositoryImpl
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.repositories.team_repository import TeamRepository
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.repositories.todo_repository import TodoRepository
from app.repositories.todo_repository_impl import TodoRepositoryImpl

from app.schemas.models.enums.priority import Priority
from app.schemas.models.enums.role import Role
from app.schemas.models.task import Task
from app.schemas.models.team import Team

from app.schemas.requests.create_task_request import CreateTodoRequest, CreateTaskRequest
from app.schemas.requests.login_user_request import LoginUserRequest
from app.schemas.requests.logout_user_request import LogoutUserRequest
from app.schemas.requests.register_user_request import RegisterUserRequest

from app.services.auth_service import AuthService
from app.services.todo_service import TodoService


from app.schemas.models.enums.status import Status
from app.schemas.requests.completed_status_request import CompletedStatusRequest


class TestTodoService:

    @pytest.fixture
    def team_member_repository(self, session: Session) -> TeamMemberRepository:
        return TeamMemberRepositoryImpl(session=session)

    @pytest.fixture
    def team_repository(
        self,
        session: Session
    ) -> TeamRepository:

        return TeamRepositoryImpl(session=session)

    @pytest.fixture
    def task_repository(
        self,
        session: Session
    ) -> TaskRepository:

        return TaskRepositoryImpl(session=session)

    @pytest.fixture
    def todo_service_repository(
        self,
        session: Session
    ) -> TodoRepository:

        return TodoRepositoryImpl(session=session)

    @pytest.fixture
    def auth_service(
        self,
        team_member_repository: TeamMemberRepository
    ) -> AuthService:

        return AuthService(team_member_repository)

    @pytest.fixture
    def todo_service(
        self,
        todo_service_repository: TodoRepository,
        task_repository: TaskRepository,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository
    ) -> TodoService:

        return TodoService(
            todo_service_repository=todo_service_repository,
            task_repository=task_repository,
            team_repository=team_repository,
            team_member_repository=team_member_repository
        )

    @pytest.fixture
    def team_setup(
        self,
        auth_service: AuthService,
        team_repository: TeamRepository,
        task_repository: TaskRepository
    ):

        lead = auth_service.register(
            RegisterUserRequest(
                email="cjlead@semicolon.com",
                name="CJ Emuedo",
                password="password",
                role=Role.LEAD
            )
        )

        auth_service.login(
            LoginUserRequest(
                email="cjlead@semicolon.com",
                password="password"
            )
        )

        member = auth_service.register(
            RegisterUserRequest(
                email="cjmember@semicolon.com",
                name="CJ Seicolon",
                password="password",
                role=Role.MEMBER
            )
        )

        team = Team(
            name="CJ Development Team",
            members_id=[lead.id, member.id],
            lead=lead.id
        )

        team_repository.save(team)

        task = Task(
            title="Build Authentication System",
            team_id=team.id
        )

        task_repository.save(task)

        return {
            "lead": lead,
            "member": member,
            "team": team,
            "task": task
        }

    def test_create_todo_successfully(
        self,
        todo_service: TodoService,
        todo_repository: TodoRepository,
        team_setup
    ):

        lead = team_setup["lead"]
        member = team_setup["member"]
        task = team_setup["task"]

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=member.id,

        )

        created_todo = todo_service.create_todo(
            request,
        )

        assert created_todo.id is not None
        assert created_todo.title == "Build Login API"
        assert created_todo.assigned_to == member.id
        assert created_todo.task_id == task.id

        todos = todo_repository.view_all()

        assert len(todos) == 1

    def test_create_todo_with_priority(
        self,
        todo_service: TodoService,
        team_setup
    ):

        lead = team_setup["lead"]
        member = team_setup["member"]
        task = team_setup["task"]

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=member.id,
            priority=Priority.HIGH
        )

        created_todo = todo_service.create_todo(
            request,
            task.id,
            lead.id
        )

        assert created_todo.priority == Priority.HIGH

    def test_create_todo_fails_when_user_is_not_logged_in(
        self,
        todo_service: TodoService,
        team_setup,
        team_member_repository: TeamMemberRepository
    ):

        lead = team_setup["lead"]
        task = team_setup["task"]

        lead.is_active = False
        team_member_repository.save(lead)

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=team_setup["member"].id
        )

        with pytest.raises(
            ValueError,
            match="User must be logged in"
        ):
            todo_service.create_todo(
                request,
                task.id,
                lead.id
            )

    def test_create_todo_fails_when_user_is_not_team_lead(
            self,
            todo_service: TodoService,
            team_setup,
            auth_service: AuthService
    ):
        member = team_setup["member"]
        task = team_setup["task"]

        auth_service.login(
            LoginUserRequest(
                email="cjmember@semicolon.com",
                password="password"
            )
        )

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=member.id
        )

        with pytest.raises(
                ValueError,
                match="Only the team lead can create a todo"
        ):
            todo_service.create_todo(
                request,
                task.id,
                member.id
            )



    def test_create_todo_fails_when_task_does_not_exist(
        self,
        todo_service: TodoService,
        team_setup
    ):

        lead = team_setup["lead"]
        member = team_setup["member"]

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=member.id
        )

        with pytest.raises(
            ValueError,
            match="Task not found"
        ):
            todo_service.create_todo(
                request,
                999,
                lead.id
            )

    def test_create_todo_fails_when_assigned_member_does_not_exist(
        self,
        todo_service: TodoService,
        team_setup
    ):

        lead = team_setup["lead"]
        task = team_setup["task"]

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=999
        )

        with pytest.raises(
            ValueError,
            match="Team member 999 not found"
        ):
            todo_service.create_todo(
                request,
                task.id,
                lead.id
            )

    def test_create_todo_fails_when_member_is_not_in_team(
        self,
        todo_service: TodoService,
        team_setup,
        auth_service: AuthService,
        team_member_repository: TeamMemberRepository
    ):

        lead = team_setup["lead"]
        task = team_setup["task"]

        outsider = auth_service.register(
            RegisterUserRequest(
                email="cjoutsider@semicolon.com",
                name="CJ Outsider",
                password="password",
                role=Role.MEMBER
            )
        )

        request = CreateTodoRequest(
            title="Build Login API",
            assigned_to=outsider.id
        )

        with pytest.raises(
            ValueError,
            match=(
                f"Team member {outsider.id} "
                f"is not a member of this team"
            )
        ):
            todo_service.create_todo(
                request,
                task.id,
                lead.id
            )






#---------------------- Test for Send Status As Completed Service -------------------------

    def register_user(self, auth_service:AuthService):
        request = RegisterUserRequest(
            name="BattyBoy",
            email="tears@semicolon.com",
            password="password",
            role=Role.LEAD
        )
        auth_service.register(request)

    def register_login_user(self, auth_service):
        self.register_user(auth_service)
        request = LoginUserRequest(
            email="tears@semicolon.com",
            password="password"
        )
        auth_service.login(request)

    def logout(self, auth_service):
        self.register_login_user(auth_service)
        request = LogoutUserRequest(
            email="tears@semicolon.com"
        )
        auth_service.logout(request)

    def a_task(self, team_repository: TeamRepository, task_repository: TaskRepository):
        team = Team(
            name="Group 6ick Of It",
            members_id=[1,2,3],
            lead=1
        )
        team_repository.save(team)

        _task = Task(
            title="Work On Team Task Board",
            team_id=1,
            due_date=datetime.datetime.now()
        )

        task_repository.save(_task)

    def a_todo(self, todo_service: TodoService):
        create_todo_request = CreateTodoRequest(
            title="Work On Create Services",
            assigned_to=1,
            due_date=datetime.date(year=2026, month=9, day=30),
            due_time=datetime.time(hour=20, minute=30),
            owner_email="tears@semicolon.com",
            current_user_id=1,
            task_id=1
        )

        return todo_service.create_todo(create_todo_request)

    def test_send_status_as_completed_doesnt_return_none(self, team_repository:TeamRepository, task_repository: TaskRepository, todo_service: TodoService, auth_service: AuthService):

        self.register_login_user(auth_service)
        self.a_task(team_repository=team_repository, task_repository=task_repository)
        self.a_todo(todo_service=todo_service)

        set_status_request = CompletedStatusRequest(todo_title="Work On Create Services", member_email="tears@semicolon.com")

        response = todo_service.send_status_as_completed(set_status_request)
        assert not response is None

    def test_send_status_for_a_valid_todo_status_is_now_pending(self, team_repository:TeamRepository, task_repository: TaskRepository, todo_service: TodoService, auth_service: AuthService):
        self.register_login_user(auth_service)
        self.a_task(team_repository=team_repository, task_repository=task_repository)
        todo = self.a_todo(todo_service=todo_service)

        assert todo.progress == Status.IN_PROGRESS

        set_status_request = CompletedStatusRequest(todo_title="Work On Create Services", member_email="tears@semicolon.com")
        response = todo_service.send_status_as_completed(set_status_request)


        assert response.status == Status.PENDING
        assert response.title is todo.title


