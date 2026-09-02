import pytest
from sqlmodel import Session

from app.repositories.todo_repository import TodoRepository
from app.repositories.todo_repository_impl import TodoRepositoryImpl
from app.schemas.models.todo import Todo


class TestTodoRepository:

    @pytest.fixture
    def todo_repository(self, session: Session) -> TodoRepository:
        return TodoRepositoryImpl(session=session)


    def test_repository_is_empty(self, todo_repository: TodoRepository):
        size = todo_repository.count()
        assert size == 0

    def test_a_todo_registration_saves_count_is_one(self, todo_repository: TodoRepository):

        todo = Todo(title='Mow the Lawn', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo)
        assert todo_repository.count() == 1

    def test_2_todo_registration_saves_count_is_two(self, todo_repository: TodoRepository):
        todo = Todo(title='Update New Request', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo)

        todo_two = Todo(title='Work On EndPoint', assigned_to="2", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo_two)

        assert todo_repository.count() == 2

    def test_delete_a_todo_from_2_total_saves_count_is_one(self, todo_repository: TodoRepository):
        todo = Todo(title='Work On Services', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo)

        todo_two = Todo(title='Work On Repository', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo_two)

        assert todo_repository.count() == 2

        todo_repository.delete(todo)
        assert todo_repository.count() == 1

    def test_find_by_id(self, todo_repository: TodoRepository):
        todo = Todo(title='Work on TodoRepository', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo)
        assert todo_repository.count() == 1

        found_todo = todo_repository.find_by_id(todo.id)
        assert found_todo == todo

    def test_find_by_todo_title(self, todo_repository: TodoRepository):
        todo = Todo(title='Work On Derailing THe Gutters', assigned_to="1", position=1, task_id=1, owner_email="test@semicolon.com")
        todo_repository.save(todo)

        found_todo = todo_repository.find_by_todo_title(todo.title)
        assert found_todo is todo