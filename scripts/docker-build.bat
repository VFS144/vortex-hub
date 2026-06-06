@echo off
REM Vortex Hub - Docker Build & Test (Windows)

echo Building Docker images...

echo Building backend image...
docker build -t vortex-hub-backend:test ./backend
if !errorlevel! neq 0 exit /b 1

echo Building frontend image...
docker build -t vortex-hub-frontend:test ./frontend
if !errorlevel! neq 0 exit /b 1

echo Images built successfully!
echo.
echo Testing Docker Compose...

docker-compose -f docker-compose.yml config > nul
if !errorlevel! neq 0 (
    echo Error: Invalid development docker-compose.yml
    exit /b 1
)
echo [OK] Development docker-compose.yml is valid

docker-compose -f docker-compose.prod.yml config > nul
if !errorlevel! neq 0 (
    echo Error: Invalid production docker-compose.prod.yml
    exit /b 1
)
echo [OK] Production docker-compose.prod.yml is valid

echo.
echo All Docker checks passed!
