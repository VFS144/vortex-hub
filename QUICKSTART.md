"""
Quick start guide
"""

# Vortex Hub - Quick Start Guide

## ⚡ ONE COMMAND - Start Everything

```bash
# Windows
./run.bat

# Mac/Linux
./run.sh
```

Done! Everything will be running:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000  
- **API Docs**: http://localhost:8000/docs

Login with: `admin` / `admin123`

---

## 🚀 Get Started in 5 Minutes (Manual Setup)

### 1. Prerequisites
```bash
# Check if you have these installed
node --version  # v18+
python --version  # 3.11+
docker --version
docker-compose --version
```

### 2. Clone or Download
```bash
cd "vortex hub"
```

### 3. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend (in one terminal)
uvicorn app.main:app --reload
```

Backend runs on: **http://localhost:8000**  
API docs available at: **http://localhost:8000/docs**

### 4. Setup Frontend (in new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:3000**

### 5. Create Admin Account
```bash
# In backend terminal, create new Python session
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
...     hashed_password=hash_password("admin123"),
...     role=UserRole.ADMIN,
...     is_active=True
... )
>>> db.add(admin)
>>> db.commit()
>>> exit()
```

### 6. Login to Application
1. Go to http://localhost:3000/login
2. Username: `admin`
3. Password: `admin123`
4. You're in! 🎉

## 📁 Project Structure

```
vortex-hub/
├── frontend/                 # React TypeScript application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand state management
│   │   ├── lib/            # Utilities (API client)
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Dependencies
│   └── vite.config.ts      # Build configuration
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/         # SQLAlchemy models (database schema)
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── routes/         # API endpoints
│   │   ├── core/           # Configuration, security, database
│   │   └── main.py         # FastAPI app initialization
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container image
│
├── docs/                    # Documentation
│   ├── SETUP.md            # Detailed setup instructions
│   ├── ARCHITECTURE.md     # System architecture
│   ├── API.md              # API reference
│   ├── DEPLOYMENT.md       # Production deployment
│   └── CONTRIBUTING.md     # Contribution guidelines
│
├── docker-compose.yml       # Local development environment
├── .env.example             # Environment variables template
└── README.md               # Project overview
```

## 🔑 Default Credentials

**Admin Account (first time setup):**
- Username: `admin`
- Password: `admin123`

⚠️ **Change these immediately in production!**

## 📚 Common Commands

### Backend
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Create database tables
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Create new admin user
python scripts/create_admin.py
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Type check
npm run type-check
```

### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose build
```

## 🌐 Available Endpoints

### Frontend Pages
- 🏠 Dashboard: http://localhost:3000/dashboard
- 📁 Projects: http://localhost:3000/projects
- ✅ Tasks: http://localhost:3000/tasks
- 🐛 Bugs: http://localhost:3000/bugs
- 📖 Lore: http://localhost:3000/lore

### Backend API
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 🔐 User Roles

| Role | Access |
|------|--------|
| **Admin** | Everything |
| **Developer** | Projects, Tasks, Bugs, Analytics |
| **Editor** | Lore, Characters, Locations, Factions |
| **Viewer** | Read-only access |

## 🎨 Design System

Cosmic/Futuristic aesthetic with:
- **Primary**: Neon Purple (#9D5CFF)
- **Secondary**: Deep Violet (#6E36D9)
- **Accent**: Electric Purple (#B87CFF)
- **Dark Mode**: Default

## 📝 Create Your First Project

1. Login as admin
2. Go to Projects page
3. Click "New Project"
4. Fill in details:
   - Name: "My Game"
   - Description: "First game project"
   - Stage: "Concept"
5. Submit
6. ✅ Project created!

## 📊 Create Your First Task

1. Go to Tasks page
2. Click "New Task"
3. Fill in details:
   - Title: "Design main menu"
   - Priority: "High"
   - Status: "Planned"
4. Submit
5. ✅ Task created!

## 🐞 Report a Bug

1. Go to Bugs page
2. Click "Report Bug"
3. Fill in details:
   - Title: "Login button not responding"
   - Description: Details
   - Severity: "High"
4. Submit
5. ✅ Bug reported!

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Mac/Linux
lsof -i :8000
kill -9 <pid>
```

### Database Connection Error
```bash
# Ensure PostgreSQL is running
# Default: localhost:5432
# User: vortex_user
# Password: vortex_password (from .env)
```

### Frontend Won't Connect to Backend
```bash
# Ensure CORS is configured
# Frontend tries: http://localhost:8000
# Update VITE_API_URL if different
```

### Clear Cache
```bash
# Frontend
# DevTools → Application → Clear Site Data

# Backend
# Clear SQLAlchemy cache
python -c "import shutil; shutil.rmtree('.pytest_cache', ignore_errors=True)"
```

## 📖 Next Steps

1. ✅ Read [SETUP.md](./docs/SETUP.md) for detailed setup
2. 📚 Read [ARCHITECTURE.md](./docs/ARCHITECTURE.md) to understand the system
3. 🔌 Read [API.md](./docs/API.md) for API reference
4. 🚀 Read [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for production deployment
5. 🤝 Read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) to contribute

## 🎯 Core Features

✅ Authentication & Authorization  
✅ Project Management  
✅ Task Tracking (Kanban, List, Calendar)  
✅ Bug Tracking  
✅ Lore Database  
✅ Asset Management  
✅ Meeting Notes  
✅ Analytics  
✅ Dark Mode  
✅ Responsive Design  

## 🔮 Coming Soon

- WebSocket real-time updates
- Content calendar for social media
- Advanced analytics dashboard
- AI-powered suggestions
- Mobile app
- Team collaboration features

## 💬 Questions?

Check the [documentation](./docs) or create an issue with details.

---

**Happy building! 🚀**

**Tagline**: Every Frame. Infinite Impact.
