#!/bin/bash
# Entrypoint script for JupyterHub
# Creates users from users.txt before starting JupyterHub

set -e

echo "=========================================="
echo "JupyterHub Entrypoint"
echo "=========================================="

# Paths
USERS_FILE=${USERS_FILE:-/srv/jupyterhub/users.txt}
DB_PATH=${JUPYTERHUB_DB_PATH:-/srv/jupyterhub/jupyterhub.sqlite}
PASSWORDS_FILE=${PASSWORDS_FILE:-/srv/jupyterhub/users_pass.txt}
HOME_BASE=${HOME_BASE:-/home}

# Clean up passwords file if it exists as a directory (from previous runs)
# This can happen if Docker volume had a directory instead of a file
if [ -d "$PASSWORDS_FILE" ]; then
    echo "Warning: $PASSWORDS_FILE exists as a directory, removing it..."
    rm -rf "$PASSWORDS_FILE" || echo "Note: Could not remove directory (may be in use)"
fi
# Also clean up if it exists as a file (to ensure fresh start)
if [ -f "$PASSWORDS_FILE" ]; then
    rm -f "$PASSWORDS_FILE" || true
fi

# Create Linux user accounts if users.txt exists
if [ -f "$USERS_FILE" ]; then
    echo "Step 1: Creating Linux user accounts..."
    python3 /srv/jupyterhub/create_linux_users.py
    echo ""
    
    echo "Step 2: Creating JupyterHub database users..."
    python3 /srv/jupyterhub/create_users.py
    echo ""
else
    echo "No users.txt found, skipping user creation."
    echo "Users can still sign up via the web interface."
    echo ""
fi

# Ensure home directory base exists with correct permissions
if [ ! -d "$HOME_BASE" ]; then
    mkdir -p "$HOME_BASE"
    chmod 755 "$HOME_BASE"
fi

# Ensure shared directories exist
mkdir -p /shared/notebooks /shared/data
chmod 755 /shared/notebooks /shared/data

# Copy shared notebooks if they exist and directory is empty
if [ -d "/shared/notebooks" ] && [ -z "$(ls -A /shared/notebooks)" ] && [ -d "/mnt/notebooks" ]; then
    cp -r /mnt/notebooks/* /shared/notebooks/ 2>/dev/null || true
fi

# Start JupyterHub
echo "Starting JupyterHub..."
exec jupyterhub -f /srv/jupyterhub/jupyterhub_config.py

