#!/usr/bin/env python3
"""
Create Linux user accounts for JupyterHub users
Ensures each user has a home directory with proper permissions
"""

import os
import subprocess
import sys
import pwd
import grp

def user_exists(username):
    """Check if Linux user exists"""
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def create_user(username, home_base='/home'):
    """Create a Linux user account with home directory"""
    if user_exists(username):
        print(f"User {username} already exists, skipping creation")
        return True
    
    home_dir = os.path.join(home_base, username)
    
    try:
        # Create user with home directory
        # -m: create home directory
        # -s /bin/bash: set shell
        # -G users: add to users group
        subprocess.run(
            ['useradd', '-m', '-s', '/bin/bash', '-G', 'users', username],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Create work directory for notebooks
        work_dir = os.path.join(home_dir, 'work')
        os.makedirs(work_dir, mode=0o755, exist_ok=True)
        
        # Create data directory symlink to shared dataset
        data_link = os.path.join(home_dir, 'data')
        if not os.path.exists(data_link):
            os.symlink('/shared/data', data_link)
        
        # Create ws-questions directory symlink to shared questions
        ws_questions_link = os.path.join(home_dir, 'ws-questions')
        if not os.path.exists(ws_questions_link):
            os.symlink('/shared/ws-questions', ws_questions_link)
        
        # Set ownership
        subprocess.run(['chown', '-R', f'{username}:users', home_dir], check=True)
        
        # Set permissions: user has RWX, group has RX, others have no access
        os.chmod(home_dir, 0o755)
        os.chmod(work_dir, 0o755)
        
        # Ensure user can write to their home directory
        subprocess.run(['chmod', 'u+w', home_dir], check=True)
        
        print(f"✓ Created user {username} with home directory {home_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create user {username}: {e.stderr.decode()}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error creating user {username}: {e}", file=sys.stderr)
        return False

def create_users_from_file(users_file, home_base='/home'):
    """Create Linux users from users.txt file"""
    
    if not os.path.exists(users_file):
        print(f"Warning: {users_file} not found. Skipping Linux user creation.")
        return []
    
    # Read users from file
    users = []
    
    with open(users_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Remove admin marker (*) if present
            if line.endswith('*'):
                username = line[:-1].strip()
            else:
                username = line.strip()
            
            if username:
                users.append(username)
    
    if not users:
        print("No users found in users.txt")
        return []
    
    # Create users
    created = []
    for username in users:
        if create_user(username, home_base):
            created.append(username)
    
    print(f"\nCreated {len(created)} Linux user accounts")
    return created

if __name__ == '__main__':
    # Check if running as root
    if os.geteuid() != 0:
        print("Error: This script must be run as root to create users", file=sys.stderr)
        sys.exit(1)
    
    # Paths
    users_file = os.getenv('USERS_FILE', '/srv/jupyterhub/users.txt')
    home_base = os.getenv('HOME_BASE', '/home')
    
    # Create users
    try:
        created = create_users_from_file(users_file, home_base)
        if created:
            print("\n✅ Linux user creation completed successfully!")
        else:
            print("\n⚠️  No users were created.")
    except Exception as e:
        print(f"\n❌ Error creating Linux users: {e}", file=sys.stderr)
        sys.exit(1)

