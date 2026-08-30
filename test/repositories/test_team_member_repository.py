import pytest
from sqlmodel import Session

from repositories.team_member_repository import TeamMemberRepository
from repositories.team_member_repository_impl import TeamMemberRepositoryImpl


class TeamMemberRepositoryTest:

    @pytest.fixture
    def team_member_repository(self, session: Session) -> TeamMemberRepository:
       return TeamMemberRepositoryImpl(session=session)


    def test_repository_is_empty(self, team_member_repository: TeamMemberRepository):
        size = team_member_repository.count()
        assert size == 0