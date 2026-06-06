"""
Setup and installation guide for Vortex Hub
"""

# Vortex Hub - Setup Guide

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+
- **Docker** & **Docker Compose** (for containerized deployment)
- **Git**

## Local Development Setup

### 1. Clone and Navigate to Project

```bash
cd "vortex hub"
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Update the `.env` file with your database credentials and JWT secret.

### 3. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create initial database
python -m alembic init -t async alembic

# Run database migrations (or use: alembic upgrade head)
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start backend server
uvicorn app.main:app --reload
```

The backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

### 5. Create First Admin User

Once the backend is running:

```bash
# In backend terminal
python
>>> from app.core.security import hash_password
>>> from app.core.database import SessionLocal
>>> from app.models import User, UserRole
>>> 
>>> db = SessionLocal()
>>> admin = User(
...     username="admin",
...     email="admin@vortexhub.local",
...     full_name="Administrator",
...     hashed_password=hash_password("changeme123"),
...     role=UserRole.ADMIN,
...     is_active=True
... )
>>> db.add(admin)
>>> db.commit()
>>> exit()
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `changeme123`

⚠️ **Change these credentials in production!**

## Docker Deployment

### Development with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Shutdown
docker-compose down
```

Services:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Database**: PostgreSQL on localhost:5432

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.yml build

# Deploy
docker-compose -f docker-compose.yml up -d
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user

### Projects
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project details
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Tasks
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Bugs
- `GET /api/bugs` - List bugs
- `POST /api/bugs` - Report bug
- `GET /api/bugs/{id}` - Get bug details
- `PATCH /api/bugs/{id}` - Update bug
- `DELETE /api/bugs/{id}` - Delete bug

## User Roles & Permissions

### Admin
- Full access to all features
- User management
- Settings configuration

### Developer
- Task management
- Bug tracking
- Project development features
- Cannot edit lore

### Editor
- Lore database access
- Character/location management
- Story content editing
- Cannot access development tools

### Viewer
- Read-only access
- Cannot modify any content

## Database Schema

The system uses PostgreSQL with SQLAlchemy ORM. Main tables:

- `users` - User accounts and authentication
- `projects` - Game projects
- `tasks` - Development tasks
- `bugs` - Bug reports
- `characters` - Lore characters
- `locations` - Game locations
- `factions` - Story factions
- `quests` - Game quests
- `assets` - File assets
- `milestones` - Project milestones
- `content_schedule` - Social media calendar

## Troubleshooting

### Port Already in Use

```bash
# Find process on port 8000
lsof -i :8000

# Find process on port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U vortex_user -d vortex_hub -c "SELECT 1;"

# Reset database
dropdb vortex_hub
createdb vortex_hub
```

### Token Issues

Clear browser localStorage and login again:

```javascript
// In browser console
localStorage.clear()
```

## Performance Tips

1. **Enable caching**: Configure Redis for session management
2. **Optimize queries**: Use database indexes on frequently queried fields
3. **API pagination**: Implement pagination for large datasets
4. **Frontend optimization**: Lazy load components and images
5. **CDN**: Use CDN for static assets in production

## Next Steps

1. Customize branding and styling
2. Add team members with appropriate roles
3. Create initial projects
4. Set up WebSocket connections for real-time updates
5. Configure backup strategy

## Support

For issues, questions, or contributions:
- Check documentation in `/docs`
- Review API docs at `/api/docs`
- Consult error logs in `backend/` and browser console

---

**Version**: 1.0.0  
**Last Updated**: 2024
