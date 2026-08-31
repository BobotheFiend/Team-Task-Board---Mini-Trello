from fastapi import Depends
from sqlmodel import Session

from app.config.settings import engine
from app.repositories.board_repository import BoardRepository
from app.repositories.board_repository_impl import BoardRepositoryImpl
from app.repositories.task_repository import TaskRepository
from app.repositories.task_repository_impl import TaskRepositoryImpl
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.repositories.team_repository import TeamRepository
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.repositories.todo_repository import TodoRepository
from app.repositories.todo_repository_impl import TodoRepositoryImpl
from app.services.auth_service import AuthService


def get_session():
    with Session(engine) as session:
        yield session

#REPOSITORY DB INJECTION
def get_team_member_repository(session: Session) -> TeamMemberRepository:
    return TeamMemberRepositoryImpl(session=session)

def get_team_repository(session: Session) -> TeamRepository:
    return TeamRepositoryImpl(session=session)

def get_task_repository(session: Session) -> TaskRepository:
    return TaskRepositoryImpl(session=session)

def get_todo_repository(session: Session) -> TodoRepository:
    return TodoRepositoryImpl(session=session)

def get_board_repository(session: Session) -> BoardRepository:
    return BoardRepositoryImpl(session=session)



# SERVICE DEPENDENCY INJECTION
def get_auth_service(repository: TeamMemberRepository = Depends(get_team_member_repository)) -> AuthService:
    return AuthService(repository)