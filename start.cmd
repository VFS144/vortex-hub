@echo off
REM Vortex Hub - Simple Starter

title Vortex Hub
color 0A
cls

echo.
echo ╔════════════════════════════════════════╗
echo ║    VORTEX HUB - Simple Quick Start     ║
echo ╚════════════════════════════════════════╝
echo.

REM Get the full python path
for /f "tokens=*" %%A in ('where python') do set PYTHON_PATH=%%A

if "%PYTHON_PATH%"=="" (
    echo [ERROR] Python not found in PATH
    echo.
    echo Please install Python from microsoft store or python.org
    echo and add it to your PATH
    pause
    exit /b 1
)

echo [✓] Found Python: %PYTHON_PATH%
echo.

REM Check backend
if not exist "backend\venv" (
    echo [1] Creating backend environment...
    cd backend
    "%PYTHON_PATH%" -m venv venv
    call venv\Scripts\activate.bat
    echo [2] Installing backend dependencies...
    pip install --upgrade pip -q
    pip install -q -r requirements.txt
    cd ..
    echo [✓] Backend ready
) else (
    echo [✓] Backend environment exists
)

echo.
echo [3] Starting backend...
start "Vortex Hub Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn app.main:app --reload"
echo.

echo [4] Starting frontend...
start "Vortex Hub Frontend" cmd /k "cd frontend && npm install --legacy-peer-deps && npm run dev"
echo.

echo.
echo ╔════════════════════════════════════════╗
echo ║  ✓ Services Started!                   ║
echo ║                                        ║
echo ║  Two new windows should have opened:   ║
echo ║  1. "Vortex Hub Backend" (port 8000)   ║
echo ║  2. "Vortex Hub Frontend" (port 3000)  ║
echo ║                                        ║
echo ║  Open in browser:                      ║
echo ║  Frontend: http://localhost:3000       ║
echo ║  Backend:  http://localhost:8000       ║
echo ║  Docs:     http://localhost:8000/docs  ║
echo ║                                        ║
echo ║  Login with: admin / admin123          ║
echo ║                                        ║
echo ║  This window can be closed.            ║
echo ╚════════════════════════════════════════╝
echo.
