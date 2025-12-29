#!/bin/bash
# Check status of all services

echo "=================================================="
echo "Data Engineering Workshop - Service Status"
echo "=================================================="
echo ""

# Check if containers are running
echo "Container Status:"
docker compose ps
echo ""

# Check Docker stats
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $(docker compose ps -q) 2>/dev/null || echo "No containers running"
echo ""

# Check service endpoints
echo "Service Endpoints:"
echo "  JupyterHub:    http://localhost:8000"
echo "  Spark Master:  http://localhost:8080"
echo "  MySQL:         localhost:3306"
echo "  Redis:         localhost:6379"
echo "  Qdrant:        http://localhost:6333"
echo "  Vespa:         http://localhost:8088"
echo "  MinIO Console: http://localhost:9001"
echo "  Adminer:       http://localhost:8089"
echo ""

# Quick health checks
echo "Quick Health Checks:"

# Check MySQL
if docker compose exec -T mysql mysqladmin ping -h localhost -u root -p${MYSQL_ROOT_PASSWORD:-rootpassword123} 2>/dev/null | grep -q "mysqld is alive"; then
    echo "  ✓ MySQL is healthy"
else
    echo "  ✗ MySQL is not responding"
fi

# Check Redis
if docker compose exec -T redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "  ✓ Redis is healthy"
else
    echo "  ✗ Redis is not responding"
fi

echo ""

