"""
Project management routes with role-based access control
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import User, Project, UserRole
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.utils.dependencies import get_current_approved_user, require_admin, require_role

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Role-based access control mapping
ROLE_PERMISSIONS = {
    UserRole.ADMINISTRATOR: ["view", "create", "edit", "delete"],
    UserRole.DEVELOPER: ["view", "create", "edit"],
    UserRole.LORE_WRITER: [],
    UserRole.ARTIST: [],
    UserRole.GAME_TESTER: ["view"],
}


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get all projects"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access projects",
        )
    
    projects = db.query(Project).all()
    return projects


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Create a new project - Developers and Admins only"""
    if "create" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create projects",
        )
    
    project_dict = project_data.dict(exclude_unset=True)
    project_dict['lead_id'] = project_data.lead_id or current_user.id
    project = Project(**project_dict)
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get project by ID"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot view projects",
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update project - Developers and Admins only"""
    if "edit" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit projects",
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check permissions - only project lead or admin can update
    if current_user.role != UserRole.ADMINISTRATOR and project.lead_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project lead or administrator can update this project",
        )
    
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Delete project - Admin only"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    db.delete(project)
    db.commit()
