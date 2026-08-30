from typing import Optional, List, Any

from sqlmodel import Session, select, func

from app.repositories.board_repository import BoardRepository
from app.schemas.models.board import Board


class BoardRepositoryImpl(BoardRepository):


    def __init__(self, session: Session):
        self.session = session

    def save(self, board: Board) -> Board:
        self.session.add(board)
        self.session.commit()
        self.session.refresh(board)
        return board

    def find_by_id(self, board_id: int) -> Optional[Board]:
        return self.session.get(Board, board_id)

    def delete(self, member:Board):
        self.session.delete(member)

    def view_all(self) -> List[Board]:
        return self.session.exec(select(Board)).all()

    def find_by_board_owner_email(self, board_owner_email: str) -> Board | None:
        select_board = select(Board).where(Board.owner_email == board_owner_email)
        found_board = self.session.exec(select_board).first() or None
        return found_board

    def count(self) -> int:
        query = select(func.count(Board.id))
        return self.session.exec(query).one()