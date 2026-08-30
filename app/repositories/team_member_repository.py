from abc import ABC, abstractmethod
from typing import List

from app.schemas.models.team_member import TeamMember


class TeamMemberRepository(ABC):
    @abstractmethod
    def save(self, team_member: TeamMember):
        ...

    @abstractmethod
    def delete(self, team_member: TeamMember):
        ...

    @abstractmethod
    def find_by_id(self, team_member_id: TeamMember):
        ...

    @abstractmethod
    def view_all(self) -> List[TeamMember]:
        ...

    @abstractmethod
    def find_by_email(self, team_member_email: str) -> TeamMember:
        ...

    @abstractmethod
    def count(self):
        ...
