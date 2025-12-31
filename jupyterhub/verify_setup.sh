#!/bin/bash
# Verification script for JupyterHub setup

set -e

echo "=========================================="
echo "JupyterHub Setup Verification"
echo "=========================================="
echo ""

# Check if JupyterHub is running
echo "1. Checking if JupyterHub container is running..."
if docker ps | grep -q jupyterhub; then
    echo "   ✅ JupyterHub container is running"
else
    echo "   ❌ JupyterHub container is NOT running"
    echo "   Run: docker-compose up -d jupyterhub"
    exit 1
fi
echo ""

# Check users.txt exists
echo "2. Checking users.txt configuration..."
if [ -f "jupyterhub/users.txt" ]; then
    USER_COUNT=$(grep -v '^#' jupyterhub/users.txt | grep -v '^$' | wc -l | xargs)
    echo "   ✅ users.txt found with $USER_COUNT users"
    echo "   Users:"
    grep -v '^#' jupyterhub/users.txt | grep -v '^$' | sed 's/^/      - /'
else
    echo "   ❌ users.txt not found"
    exit 1
fi
echo ""

# Check if Linux users were created
echo "3. Checking if Linux users exist in container..."
EXPECTED_USERS=$(grep -v '^#' jupyterhub/users.txt | grep -v '^$' | sed 's/\*$//' | xargs)
ALL_EXIST=true
for user in $EXPECTED_USERS; do
    if docker exec jupyterhub id "$user" > /dev/null 2>&1; then
        echo "   ✅ User $user exists"
    else
        echo "   ❌ User $user does NOT exist"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    echo ""
    echo "   ⚠️  Some users are missing. Try rebuilding:"
    echo "   docker-compose up -d --build jupyterhub"
    exit 1
fi
echo ""

# Check credentials file
echo "4. Checking credentials file..."
if [ -f "jupyterhub/users_pass.txt" ]; then
    echo "   ✅ users_pass.txt exists"
    echo "   Preview (first 3 lines):"
    head -3 jupyterhub/users_pass.txt | sed 's/^/      /'
else
    echo "   ❌ users_pass.txt not found"
    echo "   Try rebuilding: docker-compose up -d --build jupyterhub"
    exit 1
fi
echo ""

# Check home directories
echo "5. Checking user home directories..."
for user in $EXPECTED_USERS; do
    if docker exec jupyterhub test -d "/home/$user"; then
        echo "   ✅ /home/$user exists"
    else
        echo "   ❌ /home/$user does NOT exist"
    fi
done
echo ""

# Check shared directories
echo "6. Checking shared directories..."
if docker exec jupyterhub test -d "/shared/notebooks"; then
    NOTEBOOK_COUNT=$(docker exec jupyterhub ls /shared/notebooks | wc -l | xargs)
    echo "   ✅ /shared/notebooks exists with $NOTEBOOK_COUNT items"
else
    echo "   ⚠️  /shared/notebooks not found"
fi

if docker exec jupyterhub test -d "/shared/data"; then
    DATA_COUNT=$(docker exec jupyterhub ls /shared/data | wc -l | xargs)
    echo "   ✅ /shared/data exists with $DATA_COUNT items"
else
    echo "   ⚠️  /shared/data not found"
fi
echo ""

# Check if JupyterHub web interface is accessible
echo "7. Checking JupyterHub web interface..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|302"; then
    echo "   ✅ JupyterHub is accessible at http://localhost:8000"
else
    echo "   ⚠️  JupyterHub web interface not responding"
    echo "   Check logs: docker-compose logs jupyterhub"
fi
echo ""

# Summary
echo "=========================================="
echo "✅ Verification Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:8000 in your browser"
echo "  2. Login with credentials from jupyterhub/users_pass.txt"
echo "  3. Start exploring the notebooks!"
echo ""
echo "Admin panel: http://localhost:8000/hub/admin"
echo ""

