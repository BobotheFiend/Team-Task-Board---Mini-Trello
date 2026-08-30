from typing import Optional, List, Any

from sqlmodel import Session, select, func

from app.repositories.todo_repository import TodoRepository
from app.schemas.models.todo import Todo


class TodoRepositoryImpl(TodoRepository):


    def __init__(self, session: Session):
        self.session = session

    def save(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def find_by_id(self, todo_id: str) -> Optional[Todo]:
        return self.session.get(Todo, todo_id)

    def delete(self, member:Todo):
        self.session.delete(member)

    def view_all(self) -> List[Todo]:
        return self.session.exec(select(Todo)).all()

    def find_by_todo_title(self, todo_title: str) -> Todo | None:
        select_todo = select(Todo).where(Todo.title == todo_title)
        found_todo = self.session.exec(select_todo).first() or None
        return found_todo

    def count(self) -> int:
        query = select(func.count(Todo.id))
        return self.session.exec(query).one()