from fastapi import Depends
from sqlmodel import Session

from app.config.settings import engine

from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.repositories.task_repository_impl import TaskRepositoryImpl
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.repositories.todo_repository_impl import TodoRepositoryImpl

from app.services.auth_service import AuthService
from app.services.task_service import TaskService


def get_session():
    with Session(engine) as session:
        yield session


def get_auth_service(session: Session = Depends(get_session)):
    repository = TeamMemberRepositoryImpl(session)
    return AuthService(repository)


def get_task_service(session: Session = Depends(get_session)):
    task_repository = TaskRepositoryImpl(session)
    team_repository = TeamRepositoryImpl(session)
    team_member_repository = TeamMemberRepositoryImpl(session)
    todo_repository = TodoRepositoryImpl(session)

    return TaskService(
        task_repository=task_repository,
        team_repository=team_repository,
        team_member_repository=team_member_repository,
        todo_repository=todo_repository
    )