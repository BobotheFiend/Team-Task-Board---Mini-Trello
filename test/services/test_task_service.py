from datetime import datetime

import pytest

from app.schemas.requests.create_task_request import CreateTaskRequest, CreateTodoRequest
from app.schemas.models.task import Task
from app.schemas.models.team import Team
from app.schemas.models.team_member import TeamMember
from app.services.task_service import TaskService


class FakeTaskRepository:

    def __init__(self):
        self.tasks = []

    def find_by_task_title(self, task_title):
        for task in self.tasks:
            if task.title == task_title:
                return task
        return None

    def save(self, task):
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task


class FakeTeamRepository:

    def __init__(self, team=None):
        self.team = team

    def find_by_id(self, team_id):
        if self.team is not None and self.team.id == team_id:
            return self.team
        return None


class FakeTeamMemberRepository:

    def __init__(self, members=None):
        self.members = members or []

    def find_by_id(self, team_member_id):
        for member in self.members:
            if member.id == team_member_id:
                return member
        return None


class FakeTodoRepository:

    def __init__(self):
        self.todos = []

    def save(self, todo):
        todo.id = len(self.todos) + 1
        self.todos.append(todo)
        return todo


@pytest.fixture
def team():
    return Team(
        id=1,
        name="Development Team",
        members_id=[1, 2, 3],
        lead=1
    )


@pytest.fixture
def team_members():
    return [
        TeamMember(
            id=1,
            email="john@example.com",
            name="John",
            password="password"
        ),
        TeamMember(
            id=2,
            email="mary@example.com",
            name="Mary",
            password="password"
        ),
        TeamMember(
            id=3,
            email="peter@example.com",
            name="Peter",
            password="password"
        )
    ]


@pytest.fixture
def task_service(team, team_members):
    return TaskService(
        task_repository=FakeTaskRepository(),
        team_repository=FakeTeamRepository(team),
        team_member_repository=FakeTeamMemberRepository(team_members),
        todo_repository=FakeTodoRepository()
    )


def test_create_task_successfully(task_service):

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1
    )

    created_task = task_service.create_task(request)

    assert created_task.id == 1
    assert created_task.title == "Build Authentication System"
    assert created_task.team_id == 1


def test_create_task_with_due_date(task_service):

    due_date = datetime(2026, 9, 10, 12, 0)

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1,
        due_date=due_date
    )

    created_task = task_service.create_task(request)

    assert created_task.due_date == due_date


def test_create_task_without_todos(task_service):

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1
    )

    created_task = task_service.create_task(request)

    assert created_task.title == "Build Authentication System"


def test_create_task_fails_when_team_does_not_exist():

    task_repository = FakeTaskRepository()
    team_repository = FakeTeamRepository()
    team_member_repository = FakeTeamMemberRepository()
    todo_repository = FakeTodoRepository()

    task_service = TaskService(
        task_repository,
        team_repository,
        team_member_repository,
        todo_repository
    )

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=999
    )

    with pytest.raises(ValueError, match="Team not found"):
        task_service.create_task(request)


def test_create_task_fails_when_task_title_already_exists(task_service):

    existing_task = Task(
        id=1,
        title="Build Authentication System",
        team_id=1
    )

    task_service.task_repository.tasks.append(existing_task)

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1
    )

    with pytest.raises(
        ValueError,
        match="Task with this title already exists"
    ):
        task_service.create_task(request)


def test_create_task_fails_when_todo_member_does_not_exist(task_service):

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1,
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
        task_service.create_task(request)


def test_create_task_fails_when_todo_member_is_not_in_team(task_service):

    request = CreateTaskRequest(
        title="Build Authentication System",
        team_id=1,
        todos=[
            CreateTodoRequest(
                title="Build Login API",
                assigned_to=4
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="Team member 4 not found"
    ):
        task_service.create_task(request)

