from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, create_engine

class Settings(BaseSettings):

    TEAM_TASK_BOARD_SCHEMA: str 
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()


engine = create_engine(
    settings.TEAM_TASK_BOARD_SCHEMA,
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)