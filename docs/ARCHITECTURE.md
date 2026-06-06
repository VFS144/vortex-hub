"""
Architecture and design documentation
"""

# Vortex Hub Architecture

## System Overview

Vortex Hub is built as a modern full-stack application with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Layer (Frontend)                      │
│  React 18 + TypeScript + Tailwind + ShadCN UI + Zustand        │
└────────────────┬────────────────────────────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────────────────────────────┐
│                  API Layer (FastAPI Backend)                     │
│  REST Endpoints + WebSocket Connections + JWT Auth             │
└────────────────┬────────────────────────────────────────────────┘
                 │ SQL
┌────────────────▼────────────────────────────────────────────────┐
│                  Data Layer (PostgreSQL)                         │
│  Relational Database with SQLAlchemy ORM                        │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom cosmic theme
- **State Management**: Zustand
- **API Client**: Axios with interceptors
- **Router**: React Router v6
- **Build Tool**: Vite
- **UI Components**: Custom ShadCN-style components

### Backend
- **Framework**: FastAPI (async)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Authentication**: JWT (jose) + bcrypt
- **Async**: asyncio + uvicorn
- **Validation**: Pydantic

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: Ready for GitHub Actions, GitLab CI, Jenkins

## Database Schema

### Core Tables

#### Users
```
users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
├── role (enum: admin, developer, editor, viewer)
├── is_active
├── created_at
└── updated_at
```

#### Projects
```
projects
├── id (PK)
├── name
├── description
├── stage (enum: concept, prototype, vertical_slice, alpha, beta, release, post_launch)
├── budget
├── progress (0-100)
├── lead_id (FK: users.id)
├── created_at
└── updated_at
```

#### Tasks
```
tasks
├── id (PK)
├── title
├── description
├── status (enum: backlog, planned, in_progress, testing, blocked, done)
├── priority (enum: low, medium, high, critical)
├── project_id (FK: projects.id)
├── assigned_to (FK: users.id)
├── created_by (FK: users.id)
├── due_date
├── created_at
└── updated_at
```

#### Bugs
```
bugs
├── id (PK)
├── title
├── description
├── severity (enum: low, medium, high, critical)
├── status (enum: open, assigned, investigating, fixing, testing, resolved, closed)
├── project_id (FK: projects.id)
├── assigned_to (FK: users.id)
├── reported_by (FK: users.id)
├── reproduction_steps
├── expected_result
├── actual_result
├── created_at
└── updated_at
```

#### Lore (Characters, Locations, Factions)
```
characters / locations / factions
├── id (PK)
├── name
├── [type-specific fields]
├── project_id (FK: projects.id)
├── created_at
└── updated_at
```

## Authentication Flow

1. **Registration**
   ```
   POST /api/auth/register
   → Validate input → Hash password → Create user → Return user data
   ```

2. **Login**
   ```
   POST /api/auth/login
   → Validate credentials → Generate JWT tokens → Return tokens
   ```

3. **Token Usage**
   ```
   Request with Authorization: Bearer {token}
   → Middleware validates JWT → Extract user_id and role → Proceed
   ```

4. **Token Refresh**
   ```
   POST /api/auth/refresh
   → Validate refresh token → Generate new access token → Return tokens
   ```

## Authorization System

### Role-Based Access Control (RBAC)

Each endpoint checks user role:

```python
@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(check_permission([UserRole.ADMIN, UserRole.DEVELOPER])),
    db: Session = Depends(get_db),
):
    # Only ADMIN and DEVELOPER can create projects
    ...
```

### Permission Matrix

| Feature | Admin | Developer | Editor | Viewer |
|---------|-------|-----------|--------|--------|
| Projects | ✓ | ✓ | ✗ | ✗ |
| Tasks | ✓ | ✓ | ✗ | ✗ |
| Bugs | ✓ | ✓ | ✗ | ✗ |
| Lore | ✓ | ✗ | ✓ | ✗ |
| Analytics | ✓ | ✓ | ✓ | ✓ |
| Settings | ✓ | ✗ | ✗ | ✗ |

## Frontend Architecture

### Component Structure
```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   ├── Navbar.tsx
│   └── ProtectedRoute.tsx
├── pages/               # Page components
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   ├── ProjectsPage.tsx
│   └── ...
├── stores/              # Zustand state management
│   ├── authStore.ts
│   ├── projectStore.ts
│   └── taskStore.ts
├── lib/
│   └── api.ts           # Axios instance with interceptors
├── App.tsx
└── main.tsx
```

### State Management

Using Zustand for lightweight state management:

```typescript
const useAuthStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => { ... }
}))
```

### API Integration

Axios instance with automatic token injection:

```typescript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## Backend Architecture

### Route Organization
```
app/
├── main.py              # FastAPI app initialization
├── core/
│   ├── config.py        # Configuration management
│   ├── database.py      # Database setup
│   ├── security.py      # JWT and password hashing
│   └── __init__.py
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── project.py
│   ├── task.py
│   └── ...
├── schemas/             # Pydantic validation schemas
│   ├── auth.py
│   ├── project.py
│   └── ...
├── routes/              # API endpoints
│   ├── auth.py
│   ├── projects.py
│   ├── tasks.py
│   └── ...
└── utils/
    └── dependencies.py  # FastAPI dependencies
```

### Dependency Injection Pattern

```python
@router.get("/me")
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
```

## API Response Format

### Success Response
```json
{
  "id": 1,
  "username": "developer",
  "email": "dev@example.com",
  "role": "developer",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Invalid authentication credentials"
}
```

## Security Considerations

1. **Password Storage**: Bcrypt with salt
2. **JWT Tokens**: HS256 algorithm
3. **Token Expiration**: Short-lived access tokens + refresh tokens
4. **CORS**: Configured for frontend origins only
5. **SQL Injection**: Parameterized queries via SQLAlchemy ORM
6. **Authentication**: HTTP Bearer tokens
7. **Authorization**: Role-based access control

## Performance Optimizations

1. **Database Indexing**: Primary keys and frequently queried fields
2. **Query Optimization**: Eager loading relationships
3. **Caching**: Can add Redis for sessions
4. **API Pagination**: Implement offset/limit
5. **Frontend Lazy Loading**: Code splitting with React
6. **Asset Compression**: Gzip compression for API responses

## Scalability Strategy

### Horizontal Scaling
- Stateless backend (JWT tokens)
- Database connection pooling
- Load balancer in front of multiple backend instances
- Shared session store (Redis)

### Vertical Scaling
- Database optimization (indexes, query tuning)
- CDN for static assets
- API response caching

## Deployment Strategies

### Development
- Docker Compose for local development
- Hot reload for code changes

### Staging
- Docker containers on staging server
- PostgreSQL managed instance
- Environment parity with production

### Production
- Container orchestration (Kubernetes optional)
- Load balanced API servers
- Read replicas for database
- Automated backups
- SSL/TLS encryption

## Error Handling

### Frontend
```typescript
try {
  const response = await api.post('/api/projects', data)
} catch (err) {
  // Handle 401 (refresh token)
  // Handle 403 (permission denied)
  // Handle 400 (validation error)
  // Handle 500 (server error)
}
```

### Backend
```python
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Validation error message"
)
```

## Monitoring & Logging

Future enhancements:
- Structured logging (JSON format)
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Analytics (PostHog)
- Metrics (Prometheus)

---

**Architecture Version**: 1.0  
**Last Updated**: 2024
