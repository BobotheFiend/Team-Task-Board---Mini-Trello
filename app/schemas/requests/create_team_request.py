from sqlmodel import SQLModel


class CreateTeamRequest(SQLModel):

    team_name: str
    team_members_email: list[str]
    team_leader_email: str