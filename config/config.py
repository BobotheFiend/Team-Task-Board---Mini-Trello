from sqlmodel import SQLModel, create_engine
from urllib.parse import quote_plus

# MySQL connection string
engine = create_engine(f"mysql+pymysql://BobotheFiend:"
                       f"{quote_plus('ANIAKOR1234')}"
                       f"@127.0.0.1:3306/mini_trello_db")

# Function to create database tables from SQLModel classes
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
