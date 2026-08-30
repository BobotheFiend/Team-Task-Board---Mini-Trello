import pytest
from sqlmodel import Session

from app.repositories.board_repository import BoardRepository
from app.repositories.board_repository_impl import BoardRepositoryImpl
from app.schemas.models.board import Board


class TestBoardRepository:

    @pytest.fixture
    def board_repository(self, session: Session) -> BoardRepository:
        return BoardRepositoryImpl(session=session)


    def test_repository_is_empty(self, board_repository: BoardRepository):
        size = board_repository.count()
        assert size == 0

    def test_a_board_registration_saves_count_is_one(self, board_repository: BoardRepository):

        board = Board()
        board_repository.save(board)
        assert board_repository.count() == 1

    def test_2_board_registration_saves_count_is_two(self, board_repository: BoardRepository):
        board = Board()
        board_repository.save(board)

        board_two = Board()
        board_repository.save(board_two)

        assert board_repository.count() == 2

    def test_delete_a_board_from_2_total_saves_count_is_one(self, board_repository: BoardRepository):
        board = Board()
        board_repository.save(board)

        board_two = Board()
        board_repository.save(board_two)

        assert board_repository.count() == 2

        board_repository.delete(board)
        assert board_repository.count() == 1

