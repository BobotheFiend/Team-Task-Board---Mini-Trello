import pytest
from sqlmodel import Session

from app.repositories.team_repository import TeamRepository
from app.repositories.team_repository_impl import TeamRepositoryImpl
from app.schemas.models.team import Team


class TestTeamRepository:

    @pytest.fixture
    def team_repository(self, session: Session) -> TeamRepository:
        return TeamRepositoryImpl(session=session)

    
    def test_repository_is_empty(self, team_repository: TeamRepository):
        size = team_repository.count()
        assert size == 0

    def test_a_team_registration_saves_count_is_one(self, team_repository: TeamRepository):
    
        team = Team(name='Horizons', members=[])
        team_repository.save(team)
        assert team_repository.count() == 1

    def test_2_team_registration_saves_count_is_two(self, team_repository: TeamRepository):
        team = Team(name='Horizons', members=[])
        team_repository.save(team)

        team_two = Team(name='Orions', members=[])
        team_repository.save(team_two)

        assert team_repository.count() == 2

    def test_delete_a_team_from_2_total_saves_count_is_one(self, team_repository: TeamRepository):
        team = Team(name='Panthers', members=[])
        team_repository.save(team)

        team_two = Team(name='Wolves', members=[])
        team_repository.save(team_two)

        assert team_repository.count() == 2

        team_repository.delete(team)
        assert team_repository.count() == 1

    def test_find_by_id(self, team_repository: TeamRepository):
        team = Team(name='Alpha', members=[])
        team_repository.save(team)
        assert team_repository.count() == 1

        found_team = team_repository.find_by_id(team.id)
        assert found_team == team

    def test_find_by_team_name(self, team_repository: TeamRepository):
        team = Team(name='Omega', members=[])
        team_repository.save(team)

        found_team = team_repository.find_by_team_name(team.name)
        assert found_team is team