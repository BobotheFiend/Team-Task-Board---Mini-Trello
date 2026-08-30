from schemas.models.team_member import TeamMember
from schemas.models.enums.role import Role


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def register(self, email, name, password, role=Role.MEMBER):
        existing_member = self.repository.find_by_email(email)
        if existing_member is not None:
            raise ValueError("Email already registered")
        new_member = TeamMember(email=email, name=name, password=password, role=role, is_active=False)
        return self.repository.save(new_member)

    def login(self, email, password):
        found_member = self.repository.find_by_email(email)
        if found_member is None:
            raise ValueError("No account found with this email")
        if found_member.password != password:
            raise ValueError("Incorrect password")
        found_member.is_active = True
        return self.repository.save(found_member)

    def logout(self, email):
        found_member = self.repository.find_by_email(email)
        if found_member is None:
            raise ValueError("No account found with this email")
        found_member.is_active = False
        return self.repository.save(found_member)