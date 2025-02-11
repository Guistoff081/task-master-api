import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


# Task statuses enum
class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


# Shared properties
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_date: datetime | None = None
    status: StatusEnum = Field(default=StatusEnum.PENDING)


# Properties to receive on Task creation
class TaskCreate(TaskBase):
    pass


# Properties to receive on Task update
class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    description: str | None = Field(default=None, max_length=255)
    status: StatusEnum | None = Field(default=None)  # type: ignore


# Database model, database table inferred from class name
class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: "User" = Relationship(back_populates="tasks")


# Properties to return via API, id is always required
class TaskPublic(TaskBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class TasksPublic(SQLModel):
    data: list[TaskPublic]
    count: int
