#!/bin/bash

# ============================================
# Vortex Hub - Test Suite
# ============================================
# Run all tests for both backend and frontend

set -e  # Exit on error

echo "================================"
echo "Vortex Hub - Complete Test Suite"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
FAILED_TESTS=()
PASSED_TESTS=()

# Function to run and track tests
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Running: $test_name${NC}"
    if eval "$test_command"; then
        echo -e "${GREEN}✓ $test_name passed${NC}\n"
        PASSED_TESTS+=("$test_name")
    else
        echo -e "${RED}✗ $test_name failed${NC}\n"
        FAILED_TESTS+=("$test_name")
    fi
}

# Backend Tests
echo -e "${YELLOW}========== BACKEND TESTS ==========${NC}"

if [ -d "backend" ]; then
    cd backend
    
    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo -e "${YELLOW}Installing pytest dependencies...${NC}"
        pip install -q pytest pytest-asyncio pytest-cov
    fi
    
    run_test "Backend Unit Tests" "pytest tests/test_main.py -v"
    run_test "Backend Auth Tests" "pytest tests/test_auth.py -v"
    run_test "Backend Project Tests" "pytest tests/test_projects.py -v"
    run_test "Backend Coverage Report" "pytest tests/ --cov=app --cov-report=term-missing"
    
    cd ..
else
    echo -e "${RED}Backend directory not found${NC}"
fi

echo ""

# Frontend Tests
echo -e "${YELLOW}========== FRONTEND TESTS ==========${NC}"

if [ -d "frontend" ]; then
    cd frontend
    
    # Check if npm packages are installed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install --quiet
    fi
    
    run_test "Frontend Linting" "npm run lint"
    run_test "Frontend Type Check" "npm run type-check"
    run_test "Frontend Unit Tests" "npm run test -- --run"
    
    cd ..
else
    echo -e "${RED}Frontend directory not found${NC}"
fi

echo ""

# Summary
echo -e "${YELLOW}========== TEST SUMMARY ==========${NC}"
echo "Passed: ${#PASSED_TESTS[@]}"
echo "Failed: ${#FAILED_TESTS[@]}"
echo ""

if [ ${#FAILED_TESTS[@]} -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed:${NC}"
    for test in "${FAILED_TESTS[@]}"; do
        echo -e "  ${RED}✗${NC} $test"
    done
    exit 1
fi
