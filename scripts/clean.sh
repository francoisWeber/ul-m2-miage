#!/bin/bash
# Clean up all containers, volumes, and data

echo "=================================================="
echo "⚠️  WARNING: This will remove ALL data!"
echo "=================================================="
echo ""
echo "This will:"
echo "  - Stop all containers"
echo "  - Remove all containers"
echo "  - Remove all volumes (DATABASE DATA WILL BE LOST)"
echo "  - Remove all networks"
echo ""

read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Stopping and removing everything..."

docker compose down -v

echo ""
echo "Cleanup complete!"
echo "All data has been removed."
echo ""
echo "To start fresh: ./scripts/setup.sh && ./scripts/start.sh"
echo ""

