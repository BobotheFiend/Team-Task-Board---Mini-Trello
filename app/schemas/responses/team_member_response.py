from pydantic import BaseModel

from schemas.models.enums.role import Role


class TeamMemberResponse(BaseModel):
    id: int
    email: str
    name: str
    role: Role
    is_active: bool

    @staticmethod
    def from_team_member(team_member):
        return TeamMemberResponse(
            id=team_member.id,
            email=team_member.email,
            name=team_member.name,
            role=team_member.role,
            is_active=team_member.is_active,
        )