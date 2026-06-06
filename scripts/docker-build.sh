#!/bin/bash

# ============================================
# Vortex Hub - Docker Build & Test
# ============================================

set -e

echo "Building Docker images..."

# Build backend
echo "Building backend image..."
docker build -t vortex-hub-backend:test ./backend

# Build frontend
echo "Building frontend image..."
docker build -t vortex-hub-frontend:test ./frontend

echo "Images built successfully!"
echo ""
echo "Testing Docker Compose..."

# Test docker-compose for development
docker-compose -f docker-compose.yml config > /dev/null
echo "✓ Development docker-compose.yml is valid"

# Test docker-compose for production
docker-compose -f docker-compose.prod.yml config > /dev/null
echo "✓ Production docker-compose.prod.yml is valid"

echo ""
echo "All Docker checks passed!"
