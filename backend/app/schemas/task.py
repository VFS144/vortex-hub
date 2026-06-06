"""
Pydantic schemas for tasks
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base task schema"""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    """Task creation schema"""
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Task update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Task response schema"""
    id: int
    project_id: Optional[int]
    assigned_to: Optional[int]
    created_by: int
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
