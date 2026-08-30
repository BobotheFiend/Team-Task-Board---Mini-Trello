from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.models.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        ...

    @abstractmethod
    def delete(self, task: Task):
        ...

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        ...

    @abstractmethod
    def view_all(self) -> List[Task]:
        ...

    @abstractmethod
    def find_by_task_title(self, task_title: str) -> Task | None:
        ...

    @abstractmethod
    def count(self) -> int:
        ...