from typing import Optional, List
from sqlmodel import Session, select

from schemas.models.team_member import TeamMember


class TeamMemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, member: TeamMember):
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member

    def find_by_id(self, member_id: str) -> Optional[TeamMember]:
        return self.session.get(TeamMember, member_id)

    def delete(self, member:TeamMember):
        self.session.delete(member)

    def view_all(self) -> List[TeamMember]:
        return self.session.exec(select(TeamMember)).all()
