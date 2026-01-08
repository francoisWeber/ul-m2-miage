#!/bin/bash
# Create Linux user accounts for JupyterHub with passwords
# Reads from users.txt and generates passwords saved to users_pass.txt

# Note: Not using 'set -e' because some commands (like password generation pipes)
# can return non-zero exit codes even when successful (SIGPIPE from head)
set -u  # Exit on undefined variables

# Configuration
USERS_FILE=${USERS_FILE:-/srv/jupyterhub/users.txt}
PASSWORDS_FILE=${PASSWORDS_FILE:-/srv/jupyterhub/users_pass.txt}
HOST_PASSWORDS_FILE="/host/jupyterhub/users_pass.txt"
HOME_BASE=${HOME_BASE:-/home}

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: This script must be run as root to create users" >&2
    exit 1
fi

# Check if users file exists
if [ ! -f "$USERS_FILE" ]; then
    echo "Warning: $USERS_FILE not found. Skipping Linux user creation."
    exit 0
fi

# Salt for password generation (change this to customize passwords)
PASSWORD_SALT=${PASSWORD_SALT:-"jupyterhub-2025-secret-salt"}

# Function to generate a deterministic password from username
generate_password() {
    local username="$1"
    # Generate password: sha256(SALT + username), take first 16 chars
    local password
    password=$(echo -n "${PASSWORD_SALT}${username}" | sha256sum | cut -c1-16)
    echo "$password"
}

# Function to check if user exists
user_exists() {
    id "$1" >/dev/null 2>&1
}

# Function to set user password
set_user_password() {
    local username="$1"
    local password="$2"
    
    if echo "${username}:${password}" | chpasswd 2>&1; then
        return 0
    else
        echo "✗ Failed to set password for ${username}" >&2
        return 1
    fi
}

# Function to create a user
create_user() {
    local username="$1"
    local password="$2"
    local home_dir="${HOME_BASE}/${username}"
    
    if user_exists "$username"; then
        echo "User ${username} already exists, updating password"
        if set_user_password "$username" "$password"; then
            echo "✓ Updated password for ${username}"
            return 0
        else
            return 1
        fi
    fi
    
    # Create user with home directory
    if ! useradd -m -s /bin/bash -G users "$username" 2>&1; then
        echo "✗ Failed to create user ${username}" >&2
        return 1
    fi
    
    # Set password
    if ! set_user_password "$username" "$password"; then
        echo "⚠️  User ${username} created but password setting failed" >&2
        return 1
    fi
    
    # Create work directory for notebooks
    local work_dir="${home_dir}/work"
    mkdir -p "$work_dir"
    chmod 755 "$work_dir"
    
    # Create data directory symlink to shared dataset
    local data_link="${home_dir}/data"
    if [ ! -e "$data_link" ] && [ -d "/shared/data" ]; then
        ln -s /shared/data "$data_link"
    fi
    
    # Create ws-questions directory symlink to shared questions
    local ws_questions_link="${home_dir}/ws-questions"
    if [ ! -e "$ws_questions_link" ] && [ -d "/shared/ws-questions" ]; then
        ln -s /shared/ws-questions "$ws_questions_link"
    fi
    
    # Set ownership
    chown -R "${username}:users" "$home_dir" 2>/dev/null || true
    
    # Set permissions
    chmod 755 "$home_dir" 2>/dev/null || true
    chmod 755 "$work_dir" 2>/dev/null || true
    
    echo "✓ Created user ${username} with home directory ${home_dir}"
    return 0
}

# Read users from file and create them
echo "Reading users from ${USERS_FILE}..."

declare -a users=()
declare -a admins=()
declare -a credentials=()

while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" ]] && continue
    [[ "$line" =~ ^#.*$ ]] && continue
    
    # Check if user is admin (marked with *)
    if [[ "$line" =~ \*$ ]]; then
        username="${line%\*}"
        username="${username// /}"  # Trim spaces
        users+=("$username")
        admins+=("$username")
    else
        username="${line// /}"  # Trim spaces
        users+=("$username")
    fi
done < "$USERS_FILE"

if [ ${#users[@]} -eq 0 ]; then
    echo "No users found in users.txt"
    exit 0
fi

echo "Found ${#users[@]} users to create/update"
echo ""

# Create users with passwords
user_count=0
for username in "${users[@]}"; do
    password=$(generate_password "$username")
    
    if create_user "$username" "$password"; then
        # Check if admin
        is_admin=false
        for admin in "${admins[@]}"; do
            if [ "$admin" = "$username" ]; then
                is_admin=true
                break
            fi
        done
        
        if [ "$is_admin" = true ]; then
            credentials+=("${username}:${password}:[admin]")
        else
            credentials+=("${username}:${password}")
        fi
        ((user_count++))
    fi
done

echo ""

# Save credentials to file
if [ ${#credentials[@]} -gt 0 ]; then
    # Write to container location
    {
        echo "# JupyterHub User Credentials"
        echo "# Format: username:password [admin]"
        echo "# Generated automatically - keep this file secure!"
        echo ""
        for cred in "${credentials[@]}"; do
            # Parse credential
            IFS=':' read -r user pass admin_marker <<< "$cred"
            if [ -n "$admin_marker" ]; then
                echo "${user}:${pass} [admin]"
            else
                echo "${user}:${pass}"
            fi
        done
    } > "$PASSWORDS_FILE"
    
    echo "✅ Credentials saved to: ${PASSWORDS_FILE}"
    
    # Also copy to host location if mounted
    if [ -d "/host/jupyterhub" ]; then
        if cp "$PASSWORDS_FILE" "$HOST_PASSWORDS_FILE" 2>/dev/null; then
            echo "✅ Credentials also saved to host: ${HOST_PASSWORDS_FILE}"
        else
            echo "Warning: Could not copy passwords file to host"
        fi
    fi
fi

echo ""
echo "✅ Linux user creation completed successfully!"
echo ""
echo "📋 Summary:"
echo "   Total users: ${user_count}"
echo "   Admin users: ${#admins[@]}"
echo "   Credentials file: ${PASSWORDS_FILE}"
echo ""
echo "🔐 Students can now login to JupyterHub at http://localhost:8000"

