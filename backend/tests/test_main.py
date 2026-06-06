"""
Tests for main FastAPI application
"""
import pytest


def test_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to Vortex Hub"


def test_health(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_docs_available(client):
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client):
    """Test OpenAPI schema availability"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
