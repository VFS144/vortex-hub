"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models import User, UserStatus, UserRole
from app.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.utils.dependencies import get_current_user, get_current_approved_user, require_admin

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user - always creates with PENDING status"""
    
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username)
        | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    # Create new user with PENDING status
    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        status=UserStatus.PENDING,  # Always create as PENDING
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    if user.status == UserStatus.REJECTED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been rejected. Please contact an administrator.",
        )
    
    # Allow login for PENDING users, but they won't have access to protected routes
    access_token = create_access_token({
        "sub": user.id,
        "role": user.role.value,
        "status": user.status.value,
    })
    refresh_token = create_refresh_token({"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token_endpoint(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token"""
    payload = decode_token(data.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = int(payload.get("sub")) if payload.get("sub") else None
    user = db.query(User).filter(User.id == user_id).first() if user_id else None
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    if user.status == UserStatus.REJECTED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been rejected",
        )
    
    new_access_token = create_access_token({
        "sub": user.id,
        "role": user.role.value,
        "status": user.status.value,
    })
    new_refresh_token = create_refresh_token({"sub": user.id})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.get("/pending", response_model=List[UserResponse])
async def get_pending_users(
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Get all pending user accounts - Admin only"""
    pending_users = db.query(User).filter(User.status == UserStatus.PENDING).all()
    return pending_users


@router.post("/approve/{user_id}", response_model=UserResponse)
async def approve_user(
    user_id: int,
    assigned_role: UserRole = UserRole.GAME_TESTER,
    admin: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Approve a pending user and assign a role - Admin only"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.status != UserStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in pending status",
        )
    
    user.status = UserStatus.APPROVED
    user.role = assigned_role
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/reject/{user_id}", response_model=UserResponse)
async def reject_user(
    user_id: int,
    admin: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Reject a pending user account - Admin only"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.status != UserStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in pending status",
        )
    
    user.status = UserStatus.REJECTED
    db.commit()
    db.refresh(user)
    
    return user


@router.patch("/assign-role/{user_id}", response_model=UserResponse)
async def assign_role(
    user_id: int,
    new_role: UserRole,
    admin: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Assign or change user role - Admin only"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.status != UserStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only assign roles to approved users",
        )
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return user
