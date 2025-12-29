#!/bin/bash
# View logs for services

SERVICE=${1:-}

if [ -z "$SERVICE" ]; then
    echo "Usage: ./scripts/logs.sh [service_name]"
    echo ""
    echo "Available services:"
    echo "  - jupyterhub"
    echo "  - mysql"
    echo "  - spark-master"
    echo "  - spark-worker-1"
    echo "  - spark-worker-2"
    echo "  - qdrant"
    echo "  - vespa"
    echo "  - redis"
    echo "  - minio"
    echo ""
    echo "To view all logs: docker compose logs -f"
    echo "To view specific service: ./scripts/logs.sh mysql"
    exit 1
fi

echo "Showing logs for $SERVICE (Ctrl+C to exit)..."
docker compose logs -f "$SERVICE"

