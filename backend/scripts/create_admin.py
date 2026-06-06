"""
Project initialization scripts
"""

# Script to create admin user

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import User, UserRole, UserStatus


def create_admin(username="admin", email="admin@vortexhub.local", password="admin123"):
    """Create an admin user"""
    db = SessionLocal()
    
    # Check if user exists
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        print(f"User '{username}' already exists!")
        db.close()
        return
    
    # Create admin user
    admin = User(
        username=username,
        email=email,
        full_name="Administrator",
        hashed_password=hash_password(password),
        role=UserRole.ADMINISTRATOR,
        status=UserStatus.APPROVED,
        is_active=True,
    )
    
    db.add(admin)
    db.commit()
    db.close()
    
    print(f"✓ Admin user created!")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"\n⚠️  Change credentials in production!")


if __name__ == "__main__":
    create_admin()
