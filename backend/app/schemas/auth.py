"""
Pydantic schemas for authentication
"""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.GAME_TESTER


class UserCreate(UserBase):
    """User creation schema"""
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    status: UserStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: int  # user_id
    role: str
    status: str
    iat: int
    exp: int
