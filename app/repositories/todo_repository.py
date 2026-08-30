from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.models.todo import Todo


class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: Todo) -> Todo:
        ...

    @abstractmethod
    def delete(self, todo: Todo):
        ...

    @abstractmethod
    def find_by_id(self, todo_id: int) -> Optional[Todo]:
        ...

    @abstractmethod
    def view_all(self) -> List[Todo]:
        ...

    @abstractmethod
    def find_by_todo_title(self, todo_title: str) -> Todo | None:
        ...

    @abstractmethod
    def count(self) -> int:
        ...