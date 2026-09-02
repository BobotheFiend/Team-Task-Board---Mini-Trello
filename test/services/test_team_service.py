import pytest
from sqlmodel import Session

from app.exceptions.team_service_exception import TeamServiceException
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.repositories.team_repository import TeamRepository
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.schemas.models.enums.role import Role
from app.schemas.requests.create_team_request import CreateTeamRequest
from app.schemas.requests.login_user_request import LoginUserRequest
from app.schemas.requests.logout_user_request import LogoutUserRequest
from app.schemas.requests.register_user_request import RegisterUserRequest
from app.services.auth_service import AuthService
from app.services.team_service import TeamService



class TestTeamService:

    @pytest.fixture
    def team_repository(self, session: Session) -> TeamRepository:
        return TeamRepositoryImpl(session=session)

    @pytest.fixture
    def member_repository(self, session: Session) -> TeamMemberRepository:
        return TeamMemberRepositoryImpl(session=session)

    @pytest.fixture
    def team_service(self, team_repository: TeamRepository, member_repository: TeamMemberRepository) -> TeamService:
        return TeamService(member_repository=member_repository, repository=team_repository)

    @pytest.fixture
    def auth_service(self, member_repository: TeamMemberRepository) -> AuthService:
        return AuthService(repository=member_repository)

    def create_members(self, member_repository: TeamMemberRepository, auth_service: AuthService):

        person_one = RegisterUserRequest(name='nnamdi', role=Role.LEAD, email='nnamdi@semicolon.com', password='password')
        person_two = RegisterUserRequest(email='Cj@semicolon.com', name='CJ', password='password', role=Role.MEMBER)
        person_three = RegisterUserRequest(email='adeola@semicolon.com', name='deola', password='password', role=Role.MEMBER)

        auth_service.register(person_one)
        auth_service.register(person_two)
        auth_service.register(person_three)


    def login_register(self, member_repository:TeamMemberRepository, auth_service: AuthService):
        self.create_members(member_repository=member_repository, auth_service=auth_service)
        login_request = LoginUserRequest(email='nnamdi@semicolon.com', password='password')
        auth_service.login(login_request)

    def logout(self, member_repository:TeamMemberRepository, auth_service: AuthService):
        self.create_members(member_repository=member_repository, auth_service=auth_service)
        request = LogoutUserRequest(email='nnamdi@semicolon.com')
        auth_service.logout(request)


    def test_create_team_is_not_none(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.login_register(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['nnamdi@semicolon.com', 'Cj@semicolon.com', 'adeola@semicolon.com'], team_name="Group 6ick", team_leader_email='nnamdi@semicolon.com')

        response = team_service.create_team(request)

        assert not response is None


    def test_create_team_count_is_one(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.login_register(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['nnamdi@semicolon.com', 'Cj@semicolon.com', 'adeola@semicolon.com'],team_name="Group 6ick", team_leader_email='nnamdi@semicolon.com')

        team_service.create_team(request)

        assert team_repository.count() == 1

    def test_create_team_duplicate_name_fails(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.login_register(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['nnamdi@semicolon.com', 'Cj@semicolon.com'], team_name="Unique Team", team_leader_email='nnamdi@semicolon.com')

        team_service.create_team(request)

        with pytest.raises(TeamServiceException):
            team_service.create_team(request)

    def test_create_team_leader_not_registered_fails(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.login_register(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['Cj@semicolon.com', 'adeola@semicolon.com'], team_name="Ghost Lead Team", team_leader_email='unregistered@semicolon.com')

        with pytest.raises(TeamServiceException):
            team_service.create_team(request)

    def test_create_team_while_logged_out_fails(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.logout(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['nnamdi@semicolon.com', 'Cj@semicolon.com'], team_name="Unauthorized Team", team_leader_email='nnamdi@semicolon.com')

        with pytest.raises(TeamServiceException):
            team_service.create_team(request)

    def test_create_team_with_unregistered_member_fails(self, member_repository: TeamMemberRepository, auth_service: AuthService, team_repository: TeamRepository, team_service: TeamService):
        self.login_register(member_repository=member_repository, auth_service=auth_service)

        request = CreateTeamRequest(team_members_email=['nnamdi@semicolon.com', 'ghost.member@semicolon.com'],team_name="Mixed Team",team_leader_email='nnamdi@semicolon.com')

        with pytest.raises(TeamServiceException):
            team_service.create_team(request)

