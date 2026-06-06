"""
Task management routes with role-based access control
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import User, Task, UserRole
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.utils.dependencies import get_current_approved_user, require_admin, require_role

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Role-based access control mapping
ROLE_PERMISSIONS = {
    UserRole.ADMINISTRATOR: ["view", "create", "edit", "delete"],
    UserRole.DEVELOPER: ["view", "create", "edit", "delete"],
    UserRole.ARTIST: ["view", "create", "edit", "delete"],
    UserRole.LORE_WRITER: [],
    UserRole.GAME_TESTER: [],
}


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
    project_id: int = None,
    status: str = None,
):
    """Get tasks with optional filtering"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access tasks",
        )
    
    query = db.query(Task)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.all()
    return tasks


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Create a new task - Developers, Artists, and Admins only"""
    if "create" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create tasks",
        )
    
    task = Task(
        **task_data.dict(exclude_unset=True),
        created_by=current_user.id,
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get task by ID"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot view tasks",
        )
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update task - Artists, Developers, and Admins only"""
    if "edit" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit tasks",
        )
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Delete task"""
    if "delete" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot delete tasks",
        )
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    db.delete(task)
    db.commit()
