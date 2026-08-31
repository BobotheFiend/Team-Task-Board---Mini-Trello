import pytest
from datetime import datetime
from sqlmodel import Session

from app.repositories.task_repository import TaskRepository
from app.repositories.task_repository_impl import TaskRepositoryImpl
from app.repositories.team_repository import TeamRepository
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.repositories.todo_repository import TodoRepository
from app.repositories.todo_repository_impl import TodoRepositoryImpl

from app.schemas.models.enums.role import Role
from app.schemas.models.team import Team
from app.schemas.models.team_member import TeamMember
from app.schemas.requests.create_task_request import (
    CreateTaskRequest,
    CreateTodoRequest
)
from app.schemas.requests.login_user_request import LoginUserRequest
from app.schemas.requests.register_user_request import RegisterUserRequest

from app.services.auth_service import AuthService
from app.services.task_service import TaskService


class TestTaskService:

    @pytest.fixture
    def team_member_repository(
        self,
        session: Session
    ) -> TeamMemberRepository:

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
    def todo_repository(
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
    def task_service(
        self,
        task_repository: TaskRepository,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository,
        todo_repository: TodoRepository
    ) -> TaskService:

        return TaskService(
            task_repository=task_repository,
            team_repository=team_repository,
            team_member_repository=team_member_repository,
            todo_repository=todo_repository
        )

    @pytest.fixture
    def logged_in_team_lead(
        self,
        auth_service: AuthService,
        team_member_repository: TeamMemberRepository,
        team_repository: TeamRepository
    ) -> TeamMember:

        register_request = RegisterUserRequest(
            email="cjseicolon@semicolon.com",
            name="CJ Emuedo",
            password="password",
            role=Role.LEAD
        )

        member = auth_service.register(register_request)

        login_request = LoginUserRequest(
            email="cjseicolon@semicolon.com",
            password="password"
        )

        member = auth_service.login(login_request)

        team = Team(
            name="CJ Development Team",
            members_id=[member.id],
            lead=member.id
        )

        team_repository.save(team)

        return member

    def test_create_task_successfully(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        created_task = task_service.create_task(
            request,
            logged_in_team_lead.id
        )

        assert created_task.id is not None
        assert created_task.title == "Build Authentication System"
        assert created_task.team_id == team.id

    def test_create_task_with_due_date(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        due_date = datetime(2026, 9, 10, 12, 0)

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id,
            due_date=due_date
        )

        created_task = task_service.create_task(
            request,
            logged_in_team_lead.id
        )

        assert created_task.due_date == due_date

    def test_create_task_without_todos(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        created_task = task_service.create_task(
            request,
            logged_in_team_lead.id
        )

        assert created_task.title == "Build Authentication System"

    def test_create_task_fails_when_user_is_not_logged_in(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        logged_in_team_lead.is_active = False
        team_member_repository.save(logged_in_team_lead)

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        with pytest.raises(
            ValueError,
            match="User must be logged in"
        ):
            task_service.create_task(
                request,
                logged_in_team_lead.id
            )

    def test_create_task_fails_when_user_is_not_team_lead(
        self,
        task_service: TaskService,
        auth_service: AuthService,
        team_repository: TeamRepository,
        team_member_repository: TeamMemberRepository
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

        auth_service.login(
            LoginUserRequest(
                email="cjmember@semicolon.com",
                password="password"
            )
        )

        team = Team(
            name="CJ Another Team",
            members_id=[lead.id, member.id],
            lead=lead.id
        )

        team_repository.save(team)

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        with pytest.raises(
            ValueError,
            match="Only the team lead can create a task"
        ):
            task_service.create_task(
                request,
                member.id
            )

    def test_create_task_fails_when_team_does_not_exist(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember
    ):

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=999
        )

        with pytest.raises(
            ValueError,
            match="Team not found"
        ):
            task_service.create_task(
                request,
                logged_in_team_lead.id
            )

    def test_create_task_fails_when_task_title_already_exists(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository,
        task_repository: TaskRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        existing_request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        task_service.create_task(
            existing_request,
            logged_in_team_lead.id
        )

        duplicate_request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id
        )

        with pytest.raises(
            ValueError,
            match="Task with this title already exists"
        ):
            task_service.create_task(
                duplicate_request,
                logged_in_team_lead.id
            )

    def test_create_task_fails_when_todo_member_does_not_exist(
        self,
        task_service: TaskService,
        logged_in_team_lead: TeamMember,
        team_repository: TeamRepository
    ):

        team = team_repository.find_by_team_name(
            "CJ Development Team"
        )

        request = CreateTaskRequest(
            title="Build Authentication System",
            team_id=team.id,
            todos=[
                CreateTodoRequest(
                    title="Build Login API",
                    assigned_to=999
                )
            ]
        )

        with pytest.raises(
            ValueError,
            match="Team member 999 not found"
        ):
            task_service.create_task(
                request,
                logged_in_team_lead.id
            )

