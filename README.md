# Vortex Hub

**Every Frame. Infinite Impact.**

A production-ready studio management platform combining project management, game development tracking, lore management, bug tracking, and team collaboration.

## Overview

Vortex Hub is the central operating system for Vortex Frame Studios - a complete platform that combines:
- Project Management
- Game Development Tracking
- Lore Management
- Bug Tracking
- Team Collaboration
- Content Creation Planning
- Documentation
- Studio Analytics

## Tech Stack

### Frontend
- React 18+
- TypeScript
- Tailwind CSS
- ShadCN UI
- Vite

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication

### Deployment
- Docker & Docker Compose
- Production-ready configuration

## Color Palette

- **Primary**: Neon Purple (#9D5CFF)
- **Secondary**: Deep Violet (#6E36D9)
- **Accent**: Electric Purple (#B87CFF)
- **Background**: Void Black (#0A0614)
- **Cards**: Dark Purple (#151022)
- **Text**: White (#FFFFFF) / Light Purple (#C8B8FF)

## Features

### Authentication & Authorization
- Secure JWT-based authentication
- Role-based access control (Admin, Developer, Editor, Viewer)
- Refresh token mechanism

### Dashboard
- Customizable widget layout
- Task overview
- Project status
- Team activity
- Analytics metrics

### Project Management
- Multiple game projects
- Milestones & deadlines
- Team assignment
- Progress tracking
- Release management

### Task Management
- Kanban, Calendar, and Timeline views
- Priorities, labels, dependencies
- Subtasks & task history
- Comments & attachments

### Lore Database
- Characters, locations, factions
- Items, weapons, abilities
- Quests & story chapters
- Dialogue system
- Internal wiki linking

### Bug Tracking
- Severity levels
- Assignment & tracking
- Resolution metrics
- Reproduction steps

### Asset Management
- Upload & preview
- Tagging & filtering
- Version history

### Additional Features
- Content Calendar (social media)
- Documentation Hub
- Idea Graveyard
- Roadmap System
- Meeting Notes
- Version Tracker
- Universal Search
- Backup & Restore

## Project Structure

```
vortex-hub/
├── frontend/              # React TypeScript application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/              # FastAPI application
│   ├── app/
│   ├── requirements.txt
│   ├── main.py
│   └── .env
├── docker-compose.yml    # Local development setup
├── Dockerfile            # Production image
└── docs/                 # Documentation
```

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose

### Development

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Start with Docker Compose
cd ..
docker-compose up -d

# Frontend runs on http://localhost:3000
# Backend API on http://localhost:8000
# PostgreSQL on localhost:5432
```

### Environment Setup

Create `.env` files for both frontend and backend with necessary configuration.

## API Documentation

API docs available at `http://localhost:8000/docs` (Swagger UI)

## Contributing

Follow the studio guidelines in `docs/CONTRIBUTING.md`

## License

Proprietary - Vortex Frame Studios
# vortex-hub
