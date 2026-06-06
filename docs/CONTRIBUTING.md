"""
Contributing guidelines
"""

# Contributing to Vortex Hub

Thank you for your interest in contributing to Vortex Hub! This guide will help you get started.

## Code of Conduct

Be respectful, professional, and collaborative in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Follow the setup instructions in `SETUP.md`

## Development Guidelines

### Code Style

**Backend (Python)**
- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Format with Black: `black app/`
- Lint with flake8: `flake8 app/`

**Frontend (TypeScript/React)**
- Use ESLint and Prettier
- Run: `npm run lint`
- Follow React best practices
- Use functional components and hooks

### Commit Messages

```
[TYPE] Brief description

Detailed explanation if needed.

- Bullet points for changes
- More context

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

1. Update tests
2. Update documentation
3. Write a clear PR description
4. Reference related issues
5. Ensure CI/CD passes

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Documentation

Update docs when:
- Adding new features
- Changing API endpoints
- Modifying database schema
- Adding user-facing functionality

## Feature Development

### Adding a New Feature

1. Create database models (if needed)
2. Create Pydantic schemas
3. Create API routes
4. Create frontend components
5. Write tests
6. Update documentation

### Example: Adding a New Module

```python
# 1. backend/app/models/new_feature.py
class NewFeature(Base):
    __tablename__ = "new_features"
    ...

# 2. backend/app/schemas/new_feature.py
class NewFeatureCreate(BaseModel):
    ...

# 3. backend/app/routes/new_feature.py
@router.post("/api/new-features")
async def create_feature(...):
    ...

# 4. Include in backend/app/main.py
app.include_router(new_feature.router)

# 5. frontend/src/pages/NewFeaturePage.tsx
export default function NewFeaturePage() {
    ...
}

# 6. Update frontend/src/App.tsx with route
```

## Reporting Bugs

Include:
- Clear title
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/videos if applicable
- Environment (OS, browser, version)

## Requesting Features

Include:
- Use case
- Expected behavior
- Design mockups (if applicable)
- Implementation suggestions (optional)

## Performance Guidelines

- Minimize database queries
- Use indexes for frequently queried fields
- Implement pagination for large datasets
- Lazy load components
- Optimize images and assets

## Security Guidelines

- Never commit secrets or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Sanitize database queries
- Keep dependencies updated
- Run security audits: `npm audit`, `pip audit`

## Review Process

1. Code review by maintainers
2. Feedback and discussion
3. Implementation of requested changes
4. Approval and merge
5. Deployment to staging/production

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

- Check existing documentation
- Review closed issues
- Create a discussion
- Contact maintainers

---

**Last Updated**: 2024
