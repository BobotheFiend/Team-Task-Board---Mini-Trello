from app.exceptions.team_service_exception import TeamServiceException
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_repository import TeamRepository
from app.schemas.models.team import Team
from app.schemas.requests.create_team_request import CreateTeamRequest
from app.schemas.responses.create_team_response import CreateTeamResponse


class TeamService:

    def __init__(self, member_repository:TeamMemberRepository, repository: TeamRepository):
        self.repository = repository
        self.member_repository = member_repository

    def create_team(self, request: CreateTeamRequest):

        found_lead =self.validate_lead(request)
        self.validate_name(request)

        team_members_id = []
        team_members_email = []

        for email in request.team_members_email:
            found_member = self.member_repository.find_by_email(email)
            if found_member is None:
                raise TeamServiceException("User Not Found!!")
            team_members_id.append(found_member.id)
            team_members_email.append(found_member.email)


        team_to_create = Team(
            name=request.team_name,
            members_id=team_members_id,
            members_email=team_members_email,
            lead=found_lead.id
        )

        self.repository.save(team_to_create)

        response = CreateTeamResponse(
            team_name=request.team_name,
            team_members_email=request.team_members_email,
            lead=found_lead
        )

        return response

    def validate_lead(self, request: CreateTeamRequest):
        found_lead = self.member_repository.find_by_email(request.team_leader_email)

        if(found_lead is None):
            raise TeamServiceException("User Not Found!!")
        if(not found_lead.is_active):
            raise TeamServiceException("User Not Logged In!!")

        return found_lead

    def validate_name(self, request: CreateTeamRequest):
        found_name = self.repository.find_by_team_name(request.team_name)
        if(not found_name is None):
            raise TeamServiceException("Team Name Have Already Been Picked!!\n Try Something Else")

