"""
Tests for project endpoints
"""
import pytest


def test_create_project(client, test_user_data, test_project_data):
    """Test creating a project"""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Create project
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/projects", json=test_project_data, headers=headers)
    assert response.status_code in [200, 201]
    assert "id" in response.json() or "title" in response.json()


def test_get_projects(client, test_user_data, test_project_data):
    """Test getting projects"""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get projects
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/projects", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), (list, dict))


def test_get_projects_unauthorized(client):
    """Test getting projects without authentication"""
    response = client.get("/api/projects")
    assert response.status_code in [401, 403]


def test_create_project_unauthorized(client, test_project_data):
    """Test creating project without authentication"""
    response = client.post("/api/projects", json=test_project_data)
    assert response.status_code in [401, 403]
