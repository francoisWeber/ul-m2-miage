#!/bin/bash
# Start all services for Data Engineering Workshop

set -e

echo "=================================================="
echo "Starting Data Engineering Workshop Environment"
echo "=================================================="
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Build and start services
echo "Building and starting Docker containers..."
echo "This may take several minutes on first run..."
echo ""

docker compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "Checking service status..."
docker compose ps

echo ""
echo "=================================================="
echo "Environment is starting up!"
echo "=================================================="
echo ""
echo "Services are available at:"
echo "  - JupyterHub:    http://localhost:8000"
echo "  - Spark Master:  http://localhost:8080"
echo "  - MySQL:         localhost:3306"
echo "  - Redis:         localhost:6379"
echo "  - Qdrant:        http://localhost:6333"
echo "  - Vespa:         http://localhost:8088"
echo "  - MinIO Console: http://localhost:9001"
echo "  - Adminer:       http://localhost:8089"
echo ""
echo "Default credentials:"
echo "  JupyterHub - Username: admin, Password: admin123"
echo "  MySQL      - Username: student, Password: student123"
echo "  MinIO      - Access Key: minioadmin, Secret: minioadmin"
echo ""
echo "To view logs: docker compose logs -f [service_name]"
echo "To stop:      ./scripts/stop.sh"
echo ""

