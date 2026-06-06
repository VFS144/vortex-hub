"""
Tests for authentication endpoints
"""
import pytest


def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code in [200, 201]
    assert "access_token" in response.json() or "message" in response.json()


def test_register_duplicate_email(client, test_user_data):
    """Test registering with duplicate email"""
    # Register first user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try to register with same email
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code in [400, 409]


def test_login_success(client, test_user_data):
    """Test successful login"""
    # Register user
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code in [400, 401, 404]


def test_invalid_email_format(client):
    """Test registration with invalid email"""
    response = client.post("/api/auth/register", json={
        "email": "invalid-email",
        "password": "password123",
        "username": "testuser"
    })
    assert response.status_code in [400, 422]


def test_weak_password(client):
    """Test registration with weak password"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "123",  # Too short
        "username": "testuser"
    })
    assert response.status_code in [400, 422]
