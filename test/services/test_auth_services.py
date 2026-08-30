import pytest

from app.services.auth_service import AuthService
from app.repositories.team_member_repository import TeamMemberRepository
from schemas.models.enums.role import Role


class FakeTeamMemberRepository(TeamMemberRepository):
    def __init__(self):
        self.members = []
        self.next_id = 1

    def save(self, team_member):
        if team_member.id is None:
            team_member.id = self.next_id
            self.next_id = self.next_id + 1
            self.members.append(team_member)
        return team_member

    def delete(self, team_member):
        self.members.remove(team_member)

    def find_by_id(self, team_member_id):
        for member in self.members:
            if member.id == team_member_id:
                return member
        return None

    def find_by_email(self, team_member_email):
        for member in self.members:
            if member.email == team_member_email:
                return member
        return None

    def view_all(self):
        return self.members

    def count(self):
        return len(self.members)


class TestAuthService:

    @pytest.fixture
    def repository(self) -> TeamMemberRepository:
        return FakeTeamMemberRepository()

    @pytest.fixture
    def auth_service(self, repository: TeamMemberRepository) -> AuthService:
        return AuthService(repository)

    def test_register_creates_new_member(self, auth_service: AuthService):
        member = auth_service.register("yomi@semicolon.com", "Yomi", "password123", Role.MEMBER)
        assert member.email == "yomi@semicolon.com"
        assert member.name == "Yomi"
        assert member.is_active is False
        assert member.id is not None

    def test_register_duplicate_email_raises_error(self, auth_service: AuthService):
        auth_service.register("yomi@semicolon.com", "Yomi", "password123", Role.MEMBER)
        with pytest.raises(ValueError):
            auth_service.register("yomi@semicolon.com", "Yomi2", "password456", Role.MEMBER)

    def test_login_with_correct_credentials_succeeds(self, auth_service: AuthService):
        auth_service.register("yomi@semicolon.com", "Yomi", "password123", Role.MEMBER)
        member = auth_service.login("yomi@semicolon.com", "password123")
        assert member.is_active is True

    def test_login_with_wrong_password_raises_error(self, auth_service: AuthService):
        auth_service.register("yomi@semicolon.com", "Yomi", "password123", Role.MEMBER)
        with pytest.raises(ValueError):
            auth_service.login("yomi@semicolon.com", "wrongpassword")

    def test_login_with_nonexistent_email_raises_error(self, auth_service: AuthService):
        with pytest.raises(ValueError):
            auth_service.login("ghost@semicolon.com", "password123")

    def test_logout_sets_member_inactive(self, auth_service: AuthService):
        auth_service.register("yomi@semicolon.com", "Yomi", "password123", Role.MEMBER)
        auth_service.login("yomi@semicolon.com", "password123")
        member = auth_service.logout("yomi@semicolon.com")
        assert member.is_active is False

    def test_logout_nonexistent_email_raises_error(self, auth_service: AuthService):
        with pytest.raises(ValueError):
            auth_service.logout("ghost@semicolon.com")