from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.models.board import Board


class BoardRepository(ABC):
    @abstractmethod
    def save(self, board: Board) -> Board:
        ...

    @abstractmethod
    def delete(self, board: Board):
        ...

    @abstractmethod
    def find_by_id(self, board_id: int) -> Optional[Board]:
        ...

    @abstractmethod
    def view_all(self) -> List[Board]:
        ...

    @abstractmethod
    def find_by_board_owner_email(self, board_owner_email: str) -> Board | None:
        ...

    @abstractmethod
    def count(self) -> int:
        ...