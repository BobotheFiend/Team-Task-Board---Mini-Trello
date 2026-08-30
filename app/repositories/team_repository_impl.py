from typing import Optional, List, Any

from sqlmodel import Session, select, func

from app.repositories.team_repository import TeamRepository
from app.schemas.models.team import Team


class TeamRepositoryImpl(TeamRepository):



    def __init__(self, session: Session):
        self.session = session

    def save(self, team: Team) -> Team:
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def find_by_id(self, team_id: str) -> Optional[Team]:
        return self.session.get(Team, team_id)

    def delete(self, member:Team):
        self.session.delete(member)

    def view_all(self) -> List[Team]:
        return self.session.exec(select(Team)).all()

    def find_by_team_name(self, team_name: str) -> Team | None:
        select_team = select(Team).where(Team.name == team_name)
        found_team = self.session.exec(select_team).first() or None
        return found_team

    def count(self) -> int:
        query = select(func.count(Team.id))
        return self.session.exec(query).one()