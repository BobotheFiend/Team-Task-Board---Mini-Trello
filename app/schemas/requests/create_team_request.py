from pydantic import BaseModel, Field, EmailStr


class CreateTeamRequest(BaseModel):

    team_name: str = Field(..., min_length=3, max_length=50)
    team_members_email: list[EmailStr]
    team_leader_email: EmailStr