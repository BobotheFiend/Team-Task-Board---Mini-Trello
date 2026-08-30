from fastapi import Depends
from sqlmodel import Session

from app.config.settings import engine
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.services.auth_service import AuthService


def get_session():
    with Session(engine) as session:
        yield session


def get_auth_service(session: Session = Depends(get_session)):
    repository = TeamMemberRepositoryImpl(session)
    return AuthService(repository)