from abc import ABC, abstractmethod
from typing import List

from schemas.models.team import Team


class TeamRepository(ABC):
    @abstractmethod
    def save(self, team: Team):
        ...

    @abstractmethod
    def delete(self, team: Team):
        ...

    @abstractmethod
    def find_by_id(self, team_id: Team):
        ...

    @abstractmethod
    def view_all(self) -> List[Team]:
        ...

    @abstractmethod
    def find_by_team_name(self, team_name: str) -> Team | None:
        ...

    @abstractmethod
    def count(self):
        ...