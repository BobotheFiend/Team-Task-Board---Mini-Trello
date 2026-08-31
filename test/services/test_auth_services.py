
import pytest
from pydantic import EmailStr
from sqlmodel import Session

from app.services.auth_service import AuthService
from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.schemas.models.enums.role import Role
from app.schemas.models.team_member import TeamMember
from app.schemas.requests.register_user_request import RegisterUserRequest
from controllers.auth_controller import logout_user
from schemas.requests.login_user_request import LoginUserRequest
from schemas.requests.logout_user_request import LogoutUserRequest
class TestAuthService:

    @pytest.fixture
    def auth_service_repository(self, session:Session) -> TeamMemberRepository:
        return TeamMemberRepositoryImpl(session=session)

    @pytest.fixture
    def auth_service(self, auth_service_repository: TeamMemberRepository) -> AuthService:
        return AuthService(auth_service_repository)

    def register_user(self, auth_service: AuthService, email:EmailStr, user_name:str) -> TeamMember:
        request = RegisterUserRequest(
            email=email,
            password="password",
            role=Role.MEMBER,
            name=user_name
        )

        member = auth_service.register(request)
        return member

    def test_register_creates_new_member(self, auth_service: AuthService):
        self.register_user(auth_service, "yomi@semicolon.com", "Yomi")
        assert auth_service.repository.count() == 1

    def test_register_duplicate_email_raises_error(self, auth_service: AuthService):
        self.register_user(auth_service, "yomi@semicolon.com", "Yomi")
        with pytest.raises(ValueError):
            self.register_user(auth_service, "yomi@semicolon.com", "Yomi23")

    def test_login_with_correct_credentials_succeeds(self, auth_service: AuthService):
        self.register_user(auth_service, "yomi@semicolon.com", "Yomi")
        request = LoginUserRequest(
            email="yomi@semicolon.com",
            password="password"
        )
        member = auth_service.login(request)
        assert member.is_active is True

    def test_login_with_wrong_password_raises_error(self, auth_service: AuthService):
        self.register_user(auth_service, "yomi@semicolon.com", "Yomi")
        request = LoginUserRequest(
            email="yomi@semicolon.com",
            password="wrongpp"
        )
        with pytest.raises(ValueError):
            auth_service.login(request)

    def test_login_with_nonexistent_email_raises_error(self, auth_service: AuthService):
        request = LoginUserRequest(
            email="ghost@semicolon.com",
            password="password123"
        )
        with pytest.raises(ValueError):
            auth_service.login(request)

    def test_logout_sets_member_inactive(self, auth_service: AuthService):
        self.register_user(auth_service, "yomi@semicolon.com", "Yomi")
        request = LoginUserRequest(
            email="yomi@semicolon.com",
            password="password"
        )
        auth_service.login(request)
        logout = LogoutUserRequest(email="yomi@semicolon.com")
        member = auth_service.logout(logout)
        assert member.is_active is False
