import pytest
from sqlmodel import Session

from app.repositories.task_repository import TaskRepository
from app.repositories.task_repository_impl import TaskRepositoryImpl
from app.schemas.models.task import Task


class TestTaskRepository:

    @pytest.fixture
    def task_repository(self, session: Session) -> TaskRepository:
        return TaskRepositoryImpl(session=session)


    def test_repository_is_empty(self, task_repository: TaskRepository):
        size = task_repository.count()
        assert size == 0

    def test_a_task_registration_saves_count_is_one(self, task_repository: TaskRepository):

        task = Task(title='Mow the Lawn', team_id=1)
        task_repository.save(task)
        assert task_repository.count() == 1

    def test_2_task_registration_saves_count_is_two(self, task_repository: TaskRepository):
        task = Task(title='Update New Request', team_id=1)
        task_repository.save(task)

        task_two = Task(title='Work On EndPoint', team_id=2)
        task_repository.save(task_two)

        assert task_repository.count() == 2

    def test_delete_a_task_from_2_total_saves_count_is_one(self, task_repository: TaskRepository):
        task = Task(title='Work On Services', team_id=2)
        task_repository.save(task)

        task_two = Task(title='Work On Repository', team_id=1)
        task_repository.save(task_two)

        assert task_repository.count() == 2

        task_repository.delete(task)
        assert task_repository.count() == 1

    def test_find_by_id(self, task_repository: TaskRepository):
        task = Task(title='Work on TaskRepository', team_id=1)
        task_repository.save(task)
        assert task_repository.count() == 1

        found_task = task_repository.find_by_id(task.id)
        assert found_task == task

    def test_find_by_task_title(self, task_repository: TaskRepository):
        task = Task(title='Work On Derailing THe Gutters', team_id=1)
        task_repository.save(task)

        found_task = task_repository.find_by_task_title(task.title)
        assert found_task is task