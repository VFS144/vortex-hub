#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║     VORTEX HUB - Production Manager       ║"
echo "║     Starting all services...              ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker found. Starting with Docker Compose..."
    echo ""
    docker-compose up
    exit 0
fi

echo "Starting services manually..."
echo ""

# Create backend venv if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "[1/4] Creating backend virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Install backend dependencies
echo "[2/4] Installing backend dependencies..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
cd ..

# Install frontend dependencies
echo "[3/4] Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install -q
fi
cd ..

echo "[4/4] Starting services..."
echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║  Backend:  http://localhost:8000          ║"
echo "║  Frontend: http://localhost:3000          ║"
echo "║  API Docs: http://localhost:8000/docs     ║"
echo "║                                           ║"
echo "║  Press Ctrl+C to stop all services        ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Start backend in background
echo "Starting Backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

# Start frontend in background
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✓ All services started!"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo 'Services stopped.'; exit 0" SIGINT SIGTERM

wait
