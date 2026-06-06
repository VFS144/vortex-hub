@echo off
title Vortex Hub - Running...
echo.
echo ╔═══════════════════════════════════════════╗
echo ║     VORTEX HUB - Production Manager       ║
echo ║     Starting all services...              ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Docker found. Starting with Docker Compose...
    echo.
    docker-compose up
    exit /b
)

echo Starting services manually...
echo.

REM Create backend venv if it doesn't exist
if not exist "backend\venv" (
    echo [1/4] Creating backend virtual environment...
    cd backend
    py -m venv venv
    cd ..
)

REM Install backend dependencies
echo [2/4] Installing backend dependencies...
cd backend
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -q -r requirements.txt
cd ..

REM Install frontend dependencies
echo [3/4] Installing frontend dependencies...
cd frontend
if not exist "node_modules" (
    npm cache clean --force
    call npm install --legacy-peer-deps
)
cd ..

echo [4/4] Starting services...
echo.
echo ╔═══════════════════════════════════════════╗
echo ║  Backend:  http://localhost:8000          ║
echo ║  Frontend: http://localhost:3000          ║
echo ║  API Docs: http://localhost:8000/docs     ║
echo ║                                           ║
echo ║  Close this window to stop all services   ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Start backend
echo Starting Backend...
cd backend
call venv\Scripts\activate.bat
start "Backend" cmd /k "uvicorn app.main:app --reload"
cd ..

REM Start frontend
echo Starting Frontend...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

echo
echo ✓ All services started!
echo.
pause
