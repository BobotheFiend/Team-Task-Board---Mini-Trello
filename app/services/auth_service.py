from schemas.models.team_member import TeamMember
from schemas.models.enums.role import Role
from schemas.requests.login_user_request import LoginUserRequest
from schemas.requests.register_user_request import RegisterUserRequest


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def register(self, register_request:RegisterUserRequest):
        existing_member = self.repository.find_by_email(register_request.email)
        if existing_member is not None:
            raise ValueError("Email already registered")
        new_member = TeamMember(email=register_request.email, name=register_request.name, password=register_request.password, role=register_request.role)
        return self.repository.save(new_member)

    def login(self, request:LoginUserRequest):
        found_member = self.repository.find_by_email(request.email)
        if found_member is None:
            raise ValueError("No account found with this email")
        if found_member.password != request.password:
            raise ValueError("Incorrect password")
        found_member.is_active = True
        return self.repository.save(found_member)

    def logout(self, email):
        found_member = self.repository.find_by_email(email)
        if found_member is None:
            raise ValueError("No account found with this email")
        found_member.is_active = False
        return self.repository.save(found_member)