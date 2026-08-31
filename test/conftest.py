import pytest
from sqlmodel import SQLModel, create_engine, Session, delete

TEST_DATABASE_URL: str = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 5})
from app.schemas.models.team_member import TeamMember
from app.schemas.models.team import Team
from app.schemas.models.task import Task
from app.schemas.models.board import Board
from app.schemas.models.todo import Todo

@pytest.fixture
def session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session
