#!/bin/bash
# Setup script for Data Engineering Workshop Environment

set -e

echo "=================================================="
echo "Data Engineering Workshop - Setup Script"
echo "=================================================="
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker compose is installed
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker is installed: $(docker --version)"
echo "✓ Docker Compose is installed: $(docker compose version)"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ .env file created. Please review and update if needed."
    else
        echo "⚠️  .env.example not found. Creating default .env..."
        cat > .env << 'EOF'
COMPOSE_PROJECT_NAME=dataeng-workshop
MYSQL_ROOT_PASSWORD=rootpassword123
MYSQL_DATABASE=beer_db
MYSQL_USER=student
MYSQL_PASSWORD=student123
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_ADMIN_USER=admin
MINIO_ADMIN_PASSWORD=admin123
JUPYTERHUB_ADMIN_USER=admin
JUPYTERHUB_ADMIN_PASSWORD=admin123
EOF
        echo "✓ Default .env file created."
    fi
else
    echo "✓ .env file already exists"
fi
echo ""

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p notebooks
mkdir -p scripts/mysql
mkdir -p scripts/minio
mkdir -p vespa-config
mkdir -p logs
echo "✓ Directories created"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.sh
chmod +x scripts/mysql/*.sh 2>/dev/null || true
echo "✓ Scripts are now executable"
echo ""

echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Review .env file and update if needed"
echo "2. Run: ./scripts/start.sh"
echo "3. Access JupyterHub at http://localhost:8000"
echo ""
echo "Services will be available at:"
echo "  - JupyterHub:    http://localhost:8000"
echo "  - Spark Master:  http://localhost:8080"
echo "  - MySQL:         localhost:3306"
echo "  - Redis:         localhost:6379"
echo "  - Qdrant:        http://localhost:6333"
echo "  - Vespa:         http://localhost:8088"
echo "  - MinIO Console: http://localhost:9001"
echo "  - Adminer:       http://localhost:8089"
echo ""

