@echo off
REM Vortex Hub - Test Suite (Windows)
REM Run all tests for both backend and frontend

setlocal enabledelayedexpansion
cd /d %~dp0\..

echo.
echo ================================
echo Vortex Hub - Complete Test Suite
echo ================================
echo.

set FAILED=0
set PASSED=0

REM Backend Tests
echo.
echo ========== BACKEND TESTS ==========
if exist backend (
    cd backend
    
    echo Installing pytest dependencies if needed...
    pip show pytest >nul 2>&1 || pip install -q pytest pytest-asyncio pytest-cov
    
    echo Running Backend Unit Tests...
    pytest tests/test_main.py -v
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    echo Running Backend Auth Tests...
    pytest tests/test_auth.py -v
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    echo Running Backend Project Tests...
    pytest tests/test_projects.py -v
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    echo Running Coverage Report...
    pytest tests/ --cov=app --cov-report=term-missing
    
    cd ..
) else (
    echo Backend directory not found
)

REM Frontend Tests
echo.
echo ========== FRONTEND TESTS ==========
if exist frontend (
    cd frontend
    
    if not exist node_modules (
        echo Installing npm dependencies...
        call npm install --quiet
    )
    
    echo Running Frontend Linting...
    call npm run lint
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    echo Running Frontend Type Check...
    call npm run type-check
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    echo Running Frontend Unit Tests...
    call npm run test -- --run
    if !errorlevel! equ 0 (
        set /a PASSED+=1
    ) else (
        set /a FAILED+=1
    )
    
    cd ..
) else (
    echo Frontend directory not found
)

REM Summary
echo.
echo ========== TEST SUMMARY ==========
echo Passed: %PASSED%
echo Failed: %FAILED%
echo.

if %FAILED% equ 0 (
    echo All tests passed!
    exit /b 0
) else (
    echo Some tests failed!
    exit /b 1
)
