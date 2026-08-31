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
from app.services.task_service import TaskService


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

def get_task_service(
        team_repository: TeamRepository = Depends(get_team_repository),
        task_repository: TaskRepository = Depends(get_task_repository),
        team_member_repository: TeamMemberRepository = Depends(get_team_member_repository),
        todo_repository: TodoRepository = Depends(get_todo_repository)

    ):


    return TaskService(
        task_repository=task_repository,
        team_repository=team_repository,
        team_member_repository=team_member_repository,
        todo_repository=todo_repository
    )
