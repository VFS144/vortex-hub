"""
Pytest configuration and fixtures for testing
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set test environment
os.environ['DEBUG'] = 'false'
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['JWT_SECRET'] = 'test-secret-key'

from app.main import app
from app.core.database import Base, get_db


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create a test client with overridden dependencies"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "username": "testuser"
    }


@pytest.fixture
def test_project_data():
    """Test project data"""
    return {
        "title": "Test Project",
        "description": "A test project",
        "genre": "RPG"
    }


@pytest.fixture
def test_task_data():
    """Test task data"""
    return {
        "title": "Test Task",
        "description": "A test task",
        "priority": "high",
        "status": "todo"
    }
