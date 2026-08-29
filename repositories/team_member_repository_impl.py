from typing import Optional, List
from sqlmodel import Session, select

from repositories.team_member_repository import TeamMemberRepository
from schemas.models.team_member import TeamMember


class TeamMemberRepositoryImpl(TeamMemberRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, team_member: TeamMember) -> TeamMember:
        self.session.add(team_member)
        self.session.commit()
        self.session.refresh(team_member)
        return team_member

    def find_by_id(self, team_member_id: str) -> Optional[TeamMember]:
        return self.session.get(TeamMember, team_member_id)

    def delete(self, member:TeamMember):
        self.session.delete(member)

    def view_all(self) -> List[TeamMember]:
        return self.session.exec(select(TeamMember)).all()

    def find_by_email(self, team_member_email: str) -> TeamMember:
        select_team_member = select(TeamMember).where(TeamMember.email == team_member_email)
        found_member = self.session.exec(select_team_member).first()
        return found_member