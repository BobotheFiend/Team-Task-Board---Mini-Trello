from fastapi import APIRouter, HTTPException, Depends

from app.schemas.requests.create_task_request import CreateTaskRequest
from app.schemas.models.task import Task
from app.services.task_service import TaskService
from dependencies import get_task_service


router = APIRouter()


@router.post("/tasks", response_model=Task)
def create_task(
    request: CreateTaskRequest,
    current_user_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    try:
        created_task = task_service.create_task(
            request,
            current_user_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return created_task
