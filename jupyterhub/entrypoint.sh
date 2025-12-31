#!/bin/bash
# Entrypoint script for JupyterHub
# Creates Linux users with passwords before starting JupyterHub

set -e

echo "=========================================="
echo "JupyterHub Entrypoint"
echo "=========================================="

# Paths
USERS_FILE=${USERS_FILE:-/srv/jupyterhub/users.txt}
HOME_BASE=${HOME_BASE:-/home}

# Ensure home directory base exists
if [ ! -d "$HOME_BASE" ]; then
    mkdir -p "$HOME_BASE"
    chmod 755 "$HOME_BASE"
fi

# Create Linux user accounts from users.txt
if [ -f "$USERS_FILE" ]; then
    echo "Creating Linux user accounts..."
    /srv/jupyterhub/create_linux_users.sh
    echo ""
else
    echo "⚠️  No users.txt found at $USERS_FILE"
    echo "   Please mount a users.txt file to configure users"
    echo ""
fi

# Start JupyterHub
echo "Starting JupyterHub..."
echo "=========================================="
exec jupyterhub -f /srv/jupyterhub/jupyterhub_config.py
