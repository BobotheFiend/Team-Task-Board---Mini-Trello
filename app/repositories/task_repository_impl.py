from typing import Optional, List, Any

from sqlmodel import Session, select, func

from app.repositories.task_repository import TaskRepository
from app.schemas.models.task import Task


class TaskRepositoryImpl(TaskRepository):



    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def delete(self, member:Task):
        self.session.delete(member)

    def view_all(self) -> List[Task]:
        return self.session.exec(select(Task)).all()

    def find_by_task_title(self, task_title: str) -> Task | None:
        select_task = select(Task).where(Task.title == task_title)
        found_task = self.session.exec(select_task).first() or None
        return found_task

    def count(self) -> int:
        query = select(func.count(Task.id))
        return self.session.exec(query).one()