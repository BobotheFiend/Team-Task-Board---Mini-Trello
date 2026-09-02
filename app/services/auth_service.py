from app.repositories.team_member_repository import TeamMemberRepository
from app.schemas.models.team_member import TeamMember
from app.schemas.requests.login_user_request import LoginUserRequest
from app.schemas.requests.register_user_request import RegisterUserRequest
from app.schemas.requests.logout_user_request import LogoutUserRequest


class AuthService:
    def __init__(self, repository:TeamMemberRepository):
        self.repository = repository

    def register(self, register_request:RegisterUserRequest):
        self.validate(register_request)
        new_member = TeamMember(email=register_request.email, name=register_request.name, password=register_request.password, role=register_request.role)
        return self.repository.save(new_member)

    def login(self, request:LoginUserRequest):
        found_member = self.repository.find_by_email(request.email)
        self.validate_login(request, found_member)
        found_member.is_active = True
        return self.repository.save(found_member)

    def logout(self, request:LogoutUserRequest):
        found_member = self.repository.find_by_email(request.email)
        if found_member is None:
            raise ValueError("No account found with this email")
        found_member.is_active = False
        return self.repository.save(found_member)



    def validate(self, request:RegisterUserRequest):
        existing_member = self.repository.find_by_email(request.email)
        if existing_member is not None:
            raise ValueError("Email already registered")

    def validate_login(self,request:LoginUserRequest, member:TeamMember):
        if member is None:
            raise ValueError("No account found with this email")
        if member.password != request.password:
            raise ValueError("Incorrect password")