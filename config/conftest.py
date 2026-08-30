import pytest
from sqlmodel import Field, SQLModel, create_engine, Session

TEST_DATABASE_URL = "sqlite://./test.db"

test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture
def session():
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session