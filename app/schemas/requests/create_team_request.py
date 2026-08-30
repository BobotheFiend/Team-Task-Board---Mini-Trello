from sqlmodel import SQLModel


class CreateTodoRequest(SQLModel):

    team_name: str
    team_members_email: list[str]
    team_leader_email: list[str]