"""
API reference documentation
"""

# Vortex Hub API Reference

## Base URL
```
http://localhost:8000
```

## Authentication

All endpoints except `/api/auth/register` and `/api/auth/login` require authentication.

### Headers
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

## Endpoints

### Authentication

#### Register
```
POST /api/auth/register
```

**Request Body**
```json
{
  "username": "developer1",
  "email": "dev@example.com",
  "full_name": "John Developer",
  "password": "securepassword123",
  "role": "developer"
}
```

**Response (201)**
```json
{
  "id": 1,
  "username": "developer1",
  "email": "dev@example.com",
  "full_name": "John Developer",
  "role": "developer",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Login
```
POST /api/auth/login
```

**Request Body**
```json
{
  "username": "developer1",
  "password": "securepassword123"
}
```

**Response (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /api/auth/me
```

**Response (200)**
```json
{
  "id": 1,
  "username": "developer1",
  "email": "dev@example.com",
  "full_name": "John Developer",
  "role": "developer",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Refresh Token
```
POST /api/auth/refresh
```

**Request Body**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Projects

#### List Projects
```
GET /api/projects
```

**Response (200)**
```json
[
  {
    "id": 1,
    "name": "Vortex Alpha",
    "description": "First major release",
    "stage": "alpha",
    "budget": "$100,000",
    "progress": 65,
    "lead_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Create Project
```
POST /api/projects
```

**Request Body**
```json
{
  "name": "Vortex Beta",
  "description": "Second major release",
  "stage": "beta",
  "budget": "$150,000",
  "progress": 0,
  "lead_id": 1
}
```

**Response (200)**
```json
{
  "id": 2,
  "name": "Vortex Beta",
  "description": "Second major release",
  "stage": "beta",
  "budget": "$150,000",
  "progress": 0,
  "lead_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Get Project
```
GET /api/projects/{project_id}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "Vortex Alpha",
  "description": "First major release",
  "stage": "alpha",
  "budget": "$100,000",
  "progress": 65,
  "lead_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Project
```
PATCH /api/projects/{project_id}
```

**Request Body** (all fields optional)
```json
{
  "progress": 75,
  "stage": "beta"
}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "Vortex Alpha",
  "description": "First major release",
  "stage": "beta",
  "budget": "$100,000",
  "progress": 75,
  "lead_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T15:45:00Z"
}
```

#### Delete Project
```
DELETE /api/projects/{project_id}
```

**Response (204)**
No content

### Tasks

#### List Tasks
```
GET /api/tasks?project_id=1&status=in_progress
```

**Query Parameters**
- `project_id` (optional): Filter by project
- `status` (optional): Filter by status

**Response (200)**
```json
[
  {
    "id": 1,
    "title": "Implement combat system",
    "description": "Core combat mechanics",
    "status": "in_progress",
    "priority": "high",
    "project_id": 1,
    "assigned_to": 2,
    "created_by": 1,
    "due_date": "2024-02-15T00:00:00Z",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Create Task
```
POST /api/tasks
```

**Request Body**
```json
{
  "title": "Implement UI system",
  "description": "User interface and menus",
  "status": "planned",
  "priority": "medium",
  "project_id": 1,
  "assigned_to": 3,
  "due_date": "2024-02-20T00:00:00Z"
}
```

**Response (200)**
```json
{
  "id": 2,
  "title": "Implement UI system",
  "description": "User interface and menus",
  "status": "planned",
  "priority": "medium",
  "project_id": 1,
  "assigned_to": 3,
  "created_by": 1,
  "due_date": "2024-02-20T00:00:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Get Task
```
GET /api/tasks/{task_id}
```

**Response (200)**
```json
{
  "id": 1,
  "title": "Implement combat system",
  "description": "Core combat mechanics",
  "status": "in_progress",
  "priority": "high",
  "project_id": 1,
  "assigned_to": 2,
  "created_by": 1,
  "due_date": "2024-02-15T00:00:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Task
```
PATCH /api/tasks/{task_id}
```

**Request Body** (all fields optional)
```json
{
  "status": "testing",
  "priority": "critical"
}
```

**Response (200)**
Returns updated task object

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

**Response (204)**
No content

### Bugs

#### List Bugs
```
GET /api/bugs?project_id=1&severity=critical
```

**Query Parameters**
- `project_id` (optional): Filter by project
- `severity` (optional): Filter by severity
- `status` (optional): Filter by status

**Response (200)**
```json
[
  {
    "id": 1,
    "title": "Game crashes on load",
    "description": "Application crashes when loading level 5",
    "severity": "critical",
    "status": "investigating",
    "project_id": 1,
    "assigned_to": 2,
    "reported_by": 3,
    "reproduction_steps": "1. Load game\n2. Select Level 5\n3. Press Play",
    "expected_result": "Level loads successfully",
    "actual_result": "Application crashes",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Create Bug
```
POST /api/bugs
```

**Request Body**
```json
{
  "title": "Audio plays at wrong volume",
  "description": "Sound effects play too loudly",
  "severity": "medium",
  "status": "open",
  "project_id": 1,
  "reproduction_steps": "1. Play game\n2. Trigger sound effect",
  "expected_result": "Sound plays at normal volume",
  "actual_result": "Sound is too loud"
}
```

**Response (200)**
Returns created bug object

#### Get Bug
```
GET /api/bugs/{bug_id}
```

**Response (200)**
Returns bug object

#### Update Bug
```
PATCH /api/bugs/{bug_id}
```

**Request Body** (all fields optional)
```json
{
  "status": "fixing",
  "assigned_to": 2
}
```

**Response (200)**
Returns updated bug object

#### Delete Bug
```
DELETE /api/bugs/{bug_id}
```

**Response (204)**
No content

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "User role developer does not have permission"
}
```

### 404 Not Found
```json
{
  "detail": "Project not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

**API Version**: 1.0  
**Last Updated**: 2024
