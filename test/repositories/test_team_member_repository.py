import pytest
from sqlmodel import Session

from app.repositories.team_member_repository import TeamMemberRepository
from app.repositories.team_member_repository_impl import TeamMemberRepositoryImpl
from app.schemas.models.team_member import TeamMember


class TestTeamMemberRepository:

    @pytest.fixture
    def team_member_repository(self, session: Session) -> TeamMemberRepository:
        return TeamMemberRepositoryImpl(session=session)

    def test_repository_is_empty(self, team_member_repository: TeamMemberRepository):
        size = team_member_repository.count()
        assert size == 0

    def test_a_team_member_registration_saves_count_is_one(self, team_member_repository: TeamMemberRepository):
        user = TeamMember(name='panther', email='bobothefiend@gmail.com', password='toomany12.')
        team_member_repository.save(user)
        assert team_member_repository.count() == 1

    def test_2_team_member_registration_saves_count_is_two(self, team_member_repository: TeamMemberRepository):
        user = TeamMember(name='panther', email='bobothefiend@gmail.com', password='toomany12.')
        team_member_repository.save(user)

        user_two = TeamMember(name='Akannbi', email='Binyin@gmail.com', password='woahh2234!#$')
        team_member_repository.save(user_two)

        assert team_member_repository.count() == 2

    def test_delete_a_team_member_from_2_total_saves_count_is_one(self, team_member_repository: TeamMemberRepository):
        user = TeamMember(name='panther', email='bobothefiend@gmail.com', password='toomany12.')
        team_member_repository.save(user)

        user_two = TeamMember(name='Akannbi', email='Binyin@gmail.com', password='woahh2234!#$')
        team_member_repository.save(user_two)

        assert team_member_repository.count() == 2

        team_member_repository.delete(user)
        assert team_member_repository.count() == 1

    def test_find_by_id(self, team_member_repository: TeamMemberRepository):
        user = TeamMember(name='panther', email='bobothefiend@gmail.com', password='toomany12.')
        team_member_repository.save(user)
        assert team_member_repository.count() == 1

        found_team_member = team_member_repository.find_by_id(user.id)
        assert found_team_member == user

    def test_find_by_email(self, team_member_repository: TeamMemberRepository):
        user = TeamMember(name='Akannbi', email='Binyin@gmail.com', password='woahh2234!#$')
        team_member_repository.save(user)

        found_member = team_member_repository.find_by_email(user.email)
        assert found_member == user