import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.dependencies import CurrentUser, SessionDep
from app.models.task import (
    Task,
    TaskCreate,
    TaskPublic,
    TasksPublic,
    TaskUpdate,
)
from app.models.user import Message

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=TasksPublic)
def read_tasks(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve tasks.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Task)
        count = session.exec(count_statement).one()
        statement = select(Task).offset(skip).limit(limit)
        tasks = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Task)
            .where(Task.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Task)
            .where(Task.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        tasks = session.exec(statement).all()

    # Convert Task to TaskPublic using model_validate (as from_orm is deprecated)
    return TasksPublic(
        data=[TaskPublic.model_validate(task) for task in tasks], count=count
    )


@router.get("/{id}", response_model=TaskPublic)
def read_task(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get task by ID.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return task


@router.post("/", response_model=TaskPublic)
def create_task(
    *, session: SessionDep, current_user: CurrentUser, task_in: TaskCreate
) -> Any:
    """
    Create new task.
    """
    task = Task.model_validate(task_in, update={"owner_id": current_user.id})
    if task.status == "completed" and not task.completed_date:
        task.completed_date = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.put("/{id}", response_model=TaskPublic)
def update_task(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    task_in: TaskUpdate,
) -> Any:
    """
    Update an task.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = task_in.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_dict)
    if "status" in update_dict:
        if update_dict["status"] == "completed" and not task.completed_date:
            task.completed_date = datetime.now(UTC)
        elif update_dict["status"] == "pending":
            task.completed_date = None
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{id}")
def delete_task(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an task.
    """
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(task)
    session.commit()
    return Message(message="Task deleted successfully")
