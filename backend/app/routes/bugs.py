"""
Bug tracking routes with role-based access control
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import User, Bug, UserRole, BugStatus
from app.schemas import BugCreate, BugUpdate, BugResponse
from app.utils.dependencies import get_current_approved_user, require_role, require_admin

router = APIRouter(prefix="/api/bugs", tags=["bugs"])


# Role-based access control mapping
ROLE_PERMISSIONS = {
    UserRole.ADMINISTRATOR: ["view", "create", "edit", "mark_complete", "delete"],
    UserRole.DEVELOPER: ["view", "create", "edit", "mark_complete"],
    UserRole.GAME_TESTER: ["view", "create"],
    UserRole.LORE_WRITER: [],
    UserRole.ARTIST: [],
}


@router.get("", response_model=List[BugResponse])
async def get_bugs(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
    project_id: int = None,
    severity: str = None,
    status: str = None,
):
    """Get bugs with optional filtering - only accessible to users with view permission"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access bugs",
        )
    
    query = db.query(Bug).filter(Bug.is_deleted == False)
    
    if project_id:
        query = query.filter(Bug.project_id == project_id)
    
    if severity:
        query = query.filter(Bug.severity == severity)
    
    if status:
        query = query.filter(Bug.status == status)
    
    bugs = query.all()
    return bugs


@router.post("", response_model=BugResponse)
async def create_bug(
    bug_data: BugCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Report a new bug - Game Testers and Developers can create"""
    if "create" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create bugs",
        )
    
    bug = Bug(
        **bug_data.dict(exclude_unset=True),
        reported_by=current_user.id,
        status=BugStatus.OPEN,
    )
    
    db.add(bug)
    db.commit()
    db.refresh(bug)
    
    return bug


@router.get("/{bug_id}", response_model=BugResponse)
async def get_bug(
    bug_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get bug by ID"""
    if "view" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot view bugs",
        )
    
    bug = db.query(Bug).filter(Bug.id == bug_id, Bug.is_deleted == False).first()
    
    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug not found",
        )
    
    return bug


@router.patch("/{bug_id}", response_model=BugResponse)
async def update_bug(
    bug_id: int,
    bug_data: BugUpdate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update bug - Developers and Admins can edit"""
    if "edit" not in ROLE_PERMISSIONS.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit bugs",
        )
    
    bug = db.query(Bug).filter(Bug.id == bug_id, Bug.is_deleted == False).first()
    
    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug not found",
        )
    
    # Check for status changes
    if "status" in bug_data.dict(exclude_unset=True):
        if bug_data.status == BugStatus.COMPLETE:
            if "mark_complete" not in ROLE_PERMISSIONS.get(current_user.role, []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role {current_user.role} cannot mark bugs as complete",
                )
    
    update_data = bug_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bug, field, value)
    
    db.commit()
    db.refresh(bug)
    
    return bug


@router.delete("/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bug(
    bug_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Permanently delete a completed bug - Admin only"""
    bug = db.query(Bug).filter(Bug.id == bug_id, Bug.is_deleted == False).first()
    
    if not bug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug not found",
        )
    
    if bug.status != BugStatus.COMPLETE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only completed bugs can be deleted",
        )
    
    bug.is_deleted = True
    db.commit()
