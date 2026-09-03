
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from app.exceptions.todo_service_exception import TodoServiceException
from app.schemas.models.todo import Todo
from app.schemas.requests.completed_status_request import CompletedStatusRequest
from app.schemas.requests.create_todo_request import CreateTodoRequest
from app.services.todo_service import TodoService
from app.dependencies import get_todo_service

router = APIRouter()


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]

@router.post("/createTodo", response_model=Todo)
def create_todo(request: CreateTodoRequest, todo_service: TodoServiceDep) -> Any:
    try:
        todo_to_create = todo_service.create_todo(request)
        
    except TodoServiceException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return todo_to_create



@router.post("/changeStatus", response_model=None)
def change_status(request: CompletedStatusRequest, todo_service: TodoServiceDep) -> Any:
    try:
        send_status =  todo_service.send_status_as_completed(request)

    except TodoServiceException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return send_status.__str__()
