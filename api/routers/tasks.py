from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query

from api.core.security import get_current_user_id
from api.schemas.requests import CreateTaskRequest, UpdateTaskRequest
from api.schemas.responses import TaskResponse
from database import get_db
from database.enums.task_enums import TaskStatus
from database.operations.task_operations import insert_task, get_tasks as get_tasks_db, update_task as update_task_db, \
                                                delete_task as delete_task_db

router = APIRouter(prefix="/tasks")

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse, description="Create a new task")
async def create_new_task(
        task_data: CreateTaskRequest,
        current_user_id: int = Depends(get_current_user_id),
        db=Depends(get_db)
):
    new_task = await insert_task(db, current_user_id, task_data.title, task_data.description, task_data.due_date, task_data.status)
    return new_task


@router.get("", response_model=list[TaskResponse], description="Get all tasks for the current user")
async def get_tasks(
        status: TaskStatus = Query(None, description="Filter tasks by status"),
        due_date: date = Query(None, description="Filter tasks by due date in ISO format"),
        current_user_id: int = Depends(get_current_user_id),
        db=Depends(get_db)
):
    tasks = await get_tasks_db(db, current_user_id, status=status, due_date=due_date)
    return tasks

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse, description="Update a task")
async def update_task(
        task_id: int,
        task_data: UpdateTaskRequest,
        current_user_id: int = Depends(get_current_user_id),
        db=Depends(get_db)
):
    updated_task = await update_task_db(
        db,
        task_id,
        current_user_id,
        **task_data.model_dump(exclude_unset=True)
    )
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have task with id {task_id}")

    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a task")
async def delete_task(
        task_id: int,
        current_user_id: int = Depends(get_current_user_id),
        db=Depends(get_db)
):
    delete_success = await delete_task_db(db, task_id, current_user_id)
    if not delete_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have task with id {task_id}")

    # 204