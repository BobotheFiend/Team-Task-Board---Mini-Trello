from pydantic import BaseModel, EmailStr

from app.schemas.models.team_member import TeamMember


class CreateTeamResponse(BaseModel):
    team_name: str
    team_members_email: list[EmailStr]
    lead: TeamMember

    def __str__(self):
        return f" Welcome Aboard Team {self.team_name}\n\t\t\{self.team_members_email}nYour Team Lead is{self.lead.name}"