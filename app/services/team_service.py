from app.repositories.team_repository import TeamRepository
from app.schemas.requests.create_team_request import CreateTeamRequest


class TeamService:

    def __init__(self, repository: TeamRepository):
        self.repository = repository

    def create_team(self, request: CreateTeamRequest):
        
        ...