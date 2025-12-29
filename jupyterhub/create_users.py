#!/usr/bin/env python3
"""
Create JupyterHub users from users.txt file
Users with '*' suffix are marked as admins
Generates random passwords and saves them to users_pass.txt
"""

import os
import secrets
import string
import sqlite3
import hashlib
import sys

def generate_password(length=12):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def hash_password(password):
    """Hash password using SHA256 (NativeAuthenticator format)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_users(users_file, db_path, passwords_file):
    """Create users in JupyterHub database"""
    
    if not os.path.exists(users_file):
        print(f"Warning: {users_file} not found. Skipping user creation.")
        return []
    
    # Read users from file
    users = []
    admins = []
    
    with open(users_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check if user is admin (marked with *)
            if line.endswith('*'):
                username = line[:-1].strip()
                admins.append(username)
            else:
                username = line.strip()
            
            if username:
                users.append(username)
    
    if not users:
        print("No users found in users.txt")
        return []
    
    # Connect to database
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, mode=0o755)
    
    # Create credentials
    credentials = []
    
    for username in users:
        # Generate random password
        password = generate_password()
        
        # Hash password
        password_hash = hash_password(password)
        
        # Check if user is admin
        is_admin = 1 if username in admins else 0
        credentials.append((username, password, is_admin))
        print(f"Created user: {username} {'(admin)' if is_admin else ''}")
    
    # Save credentials to file
    # Remove file/directory if it exists (can happen if volume had a directory from previous run)
    if os.path.exists(passwords_file):
        import shutil
        if os.path.isdir(passwords_file):
            print(f"Warning: {passwords_file} exists as a directory, removing it...")
            shutil.rmtree(passwords_file)
        elif os.path.isfile(passwords_file):
            # Remove existing file to overwrite
            os.remove(passwords_file)
    
    # Ensure parent directory exists
    passwords_dir = os.path.dirname(passwords_file)
    if passwords_dir and not os.path.exists(passwords_dir):
        os.makedirs(passwords_dir, mode=0o755, exist_ok=True)
    
    # Double-check: if it still exists as directory, try to remove again
    if os.path.exists(passwords_file) and os.path.isdir(passwords_file):
        import shutil
        print(f"Error: {passwords_file} is still a directory after cleanup attempt")
        shutil.rmtree(passwords_file)
    
    # Write credentials to file
    try:
        with open(passwords_file, 'w') as f:
            f.write("# JupyterHub User Credentials\n")
            f.write("# Format: username:password [admin]\n")
            f.write("# Generated automatically - keep this file secure!\n\n")
            for username, password, is_admin in credentials:
                admin_marker = " [admin]" if is_admin else ""
                f.write(f"{username}:{password}{admin_marker}\n")
    except IsADirectoryError:
        # If it's still a directory, try one more time with force removal
        import shutil
        print(f"Error: {passwords_file} is a directory. Force removing...")
        if os.path.exists(passwords_file):
            shutil.rmtree(passwords_file)
        # Try writing again
        with open(passwords_file, 'w') as f:
            f.write("# JupyterHub User Credentials\n")
            f.write("# Format: username:password [admin]\n")
            f.write("# Generated automatically - keep this file secure!\n\n")
            for username, password, is_admin in credentials:
                admin_marker = " [admin]" if is_admin else ""
                f.write(f"{username}:{password}{admin_marker}\n")
    
    print(f"\nCredentials saved to: {passwords_file}")
    print(f"Total users created: {len(users)}")
    print(f"Admin users: {len(admins)}")
    
    return credentials

if __name__ == '__main__':
    # Paths
    users_file = os.getenv('USERS_FILE', '/srv/jupyterhub/users.txt')
    db_path = os.getenv('JUPYTERHUB_DB_PATH', '/srv/jupyterhub/jupyterhub.sqlite')
    # Write to both container location and host location
    passwords_file_container = os.getenv('PASSWORDS_FILE', '/srv/jupyterhub/users_pass.txt')
    passwords_file_host = '/host/jupyterhub/users_pass.txt'
    
    # Create users
    try:
        credentials = create_users(users_file, db_path, passwords_file_container)
        
        # Also copy to host location if mounted
        if credentials and os.path.exists('/host/jupyterhub'):
            try:
                host_passwords_file = passwords_file_host
                # Remove if exists as directory
                if os.path.exists(host_passwords_file) and os.path.isdir(host_passwords_file):
                    import shutil
                    shutil.rmtree(host_passwords_file)
                
                # Copy file to host
                import shutil
                shutil.copy2(passwords_file_container, host_passwords_file)
                print(f"Credentials also saved to host: {host_passwords_file}")
            except Exception as e:
                print(f"Warning: Could not copy passwords file to host: {e}")
        
        if credentials:
            print("\n✅ User creation completed successfully!")
        else:
            print("\n⚠️  No users were created.")
    except Exception as e:
        print(f"\n❌ Error creating users: {e}", file=sys.stderr)
        sys.exit(1)

