# Vortex Hub - Testing Guide

## Running Tests

### Quick Test Everything

```bash
# Linux/Mac
./scripts/test.sh

# Windows
scripts\test.bat
```

### Backend Testing

#### Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Run Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_auth.py -v

# Specific test
pytest tests/test_auth.py::test_register_user -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Watch mode
pytest-watch tests/
```

#### Test Structure
```
backend/tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_main.py          # Main app tests
├── test_auth.py          # Authentication tests
└── test_projects.py      # Project tests
```

#### Writing Tests
```python
import pytest
from fastapi.testclient import TestClient

def test_example(client, test_user_data):
    """Test example"""
    response = client.post("/api/endpoint", json=test_user_data)
    assert response.status_code == 200
    assert "data" in response.json()
```

### Frontend Testing

#### Setup
```bash
cd frontend
npm install
```

#### Run Tests
```bash
# All tests
npm run test

# Specific test file
npm run test -- api.test.ts

# Watch mode
npm run test -- --watch

# With UI
npm run test:ui

# Coverage
npm run test:coverage
```

#### Test Structure
```
frontend/src/test/
├── setup.ts              # Test configuration
├── api.test.ts           # API tests
└── components.test.ts    # Component tests
```

#### Writing Tests
```typescript
import { describe, it, expect } from 'vitest';

describe('Feature', () => {
  it('should do something', () => {
    expect(true).toBe(true);
  });
});
```

---

## CI/CD Testing

### GitHub Actions

Tests run automatically on:
- `push` to `main` or `develop` branch
- `pull_request` to `main` or `develop` branch
- Manual trigger via `workflow_dispatch`

### View CI Results
```
https://github.com/yourusername/vortex-hub/actions
```

### Workflows

**CI Pipeline** (`.github/workflows/ci.yml`)
- Backend tests with pytest
- Frontend tests with vitest
- Linting and type checking
- Security scanning with Trivy
- Docker build verification

**Deploy Pipeline** (`.github/workflows/deploy.yml`)
- Builds and pushes Docker images
- Deploys to production
- Creates GitHub releases

---

## Test Coverage

### Backend Coverage
```bash
cd backend
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

### Frontend Coverage
```bash
cd frontend
npm run test:coverage

# View HTML report
open coverage/index.html
```

### Coverage Goals
- Backend: ≥ 80%
- Frontend: ≥ 70%

---

## Docker Testing

### Build Docker Images
```bash
# Linux/Mac
./scripts/docker-build.sh

# Windows
scripts\docker-build.bat
```

### Test Docker Compose
```bash
# Validate development config
docker-compose -f docker-compose.yml config

# Validate production config
docker-compose -f docker-compose.prod.yml config

# Start services
docker-compose up -d

# Run tests inside containers
docker-compose exec backend pytest tests/
docker-compose exec frontend npm run test
```

---

## Performance Testing

### Backend Performance
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Load test
ab -n 1000 -c 10 http://localhost:8000/

# Measure response time
time curl http://localhost:8000/health
```

### Frontend Performance
```bash
# Use Lighthouse
npm install -g lighthouse

lighthouse http://localhost:3000
```

---

## Database Testing

### Test Database Queries
```bash
# Connect to test database
psql postgresql://vortex_user:vortex_password@localhost/vortex_hub

# Run query
SELECT * FROM users;

# Check indexes
\d users
```

### Test Migrations
```bash
cd backend

# Create migration
alembic revision --autogenerate -m "Add column"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Integration Testing

### Full Stack Test
```bash
# 1. Start all services
docker-compose up -d

# 2. Wait for services to be ready
sleep 10

# 3. Run integration tests
cd backend
pytest tests/ -v --tb=short

cd ../frontend
npm run test

# 4. Clean up
docker-compose down
```

### Manual Testing Checklist
- [ ] User registration works
- [ ] Login/logout works
- [ ] Create project works
- [ ] Create task works
- [ ] Create bug report works
- [ ] Lore creation works
- [ ] User can view dashboard
- [ ] API documentation loads
- [ ] CORS headers are present
- [ ] Database persists data

---

## Debugging

### Backend Debugging
```bash
# Run with debug logging
DEBUG=true docker-compose up backend

# Use Python debugger
import pdb; pdb.set_trace()

# View database queries
# Set echo=True in database.py
```

### Frontend Debugging
```bash
# Use React DevTools
npm install react-devtools

# Browser console
F12 or Cmd+Shift+I

# View network requests
Network tab in DevTools
```

### Docker Debugging
```bash
# View logs
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Inspect container
docker inspect vortex-hub-backend-dev
```

---

## Automated Testing Schedule

### Daily
- Run full test suite
- Check code coverage
- Verify health checks

### Weekly
- Performance tests
- Security scanning
- Database optimization

### Monthly
- Load testing
- Backup verification
- Dependency updates

---

## Test Data

### Seed Database
```bash
# Create admin user
cd backend
python scripts/create_admin.py

# Insert test data
python scripts/seed_data.py
```

### Test Users
```
Admin:    admin@vortex.com / admin123
User:     user@vortex.com / user123
```

---

## Continuous Integration Setup

### Local Pre-commit Hook
```bash
# Create .git/hooks/pre-commit
#!/bin/bash
npm run lint
npm run type-check
cd ../backend
pytest tests/ -q
```

### GitHub Branch Protection
- Require status checks to pass
- Require code review
- Dismiss stale pull request approvals

Last Updated: May 31, 2026
