#!/bin/bash
# Stop all services for Data Engineering Workshop

echo "=================================================="
echo "Stopping Data Engineering Workshop Environment"
echo "=================================================="
echo ""

docker compose down

echo ""
echo "All services stopped."
echo "Data is preserved in Docker volumes."
echo ""
echo "To start again: ./scripts/start.sh"
echo "To remove all data: ./scripts/clean.sh"
echo ""

