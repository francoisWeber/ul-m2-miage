import os

# JupyterHub configuration file for data engineering workshops

# ============================================================================
# General Configuration
# ============================================================================

# The public facing URL of the whole JupyterHub application
c.JupyterHub.bind_url = 'http://0.0.0.0:8000'

# Allow named servers (optional - allows users to have multiple notebooks)
c.JupyterHub.allow_named_servers = True

# Maximum number of named servers per user
c.JupyterHub.named_server_limit_per_user = 3

# ============================================================================
# Authentication
# ============================================================================

# Use Native Authenticator (simple username/password)
# For production, consider using more robust authentication
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

# Allow anyone to sign up (good for workshops)
# For production, set to False and manually create accounts
c.Authenticator.open_signup = True

# Minimum password length
c.Authenticator.minimum_password_length = 6

# Load admin users from database (set by create_users.py)
# The entrypoint script creates users before JupyterHub starts, so the database should exist
def load_admin_users():
    """Load admin users from the database"""
    import sqlite3
    db_path = os.getenv('JUPYTERHUB_DB_PATH', '/srv/jupyterhub/jupyterhub.sqlite')
    admin_users = set()
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                cursor.execute('SELECT name FROM users WHERE admin = 1')
                admins = cursor.fetchall()
                admin_users = {admin[0] for admin in admins}
            conn.close()
        except Exception as e:
            print(f"Warning: Could not load admin users from database: {e}")
    
    # Add default admin if not in database (fallback)
    if 'admin' not in admin_users:
        admin_users.add('admin')
    
    return admin_users

# Set admin users (loaded from database created by create_users.py)
c.Authenticator.admin_users = load_admin_users()

# ============================================================================
# Spawner Configuration - Local Process Spawner
# ============================================================================

# Use LocalProcessSpawner (not SimpleLocalProcessSpawner) to support user switching
from jupyterhub.spawner import LocalProcessSpawner

# Custom spawner to handle user-specific directories and permissions
class CustomLocalProcessSpawner(LocalProcessSpawner):
    @property
    def notebook_dir(self):
        """Get notebook directory for user"""
        username = self.user.name
        work_dir = f'/home/{username}/work'
        # Ensure directory exists with proper permissions
        import os
        os.makedirs(work_dir, mode=0o755, exist_ok=True)
        
        # Set ownership to user (if running as root)
        try:
            import pwd
            import subprocess
            uid = pwd.getpwnam(username).pw_uid
            gid = pwd.getpwnam(username).pw_gid
            os.chown(work_dir, uid, gid)
            # Ensure user has write permissions
            os.chmod(work_dir, 0o755)
        except Exception as e:
            print(f"Warning: Could not set ownership for {work_dir}: {e}")
        
        # Copy shared notebooks if work directory is empty
        shared_notebooks = '/shared/notebooks'
        if os.path.exists(shared_notebooks):
            try:
                items = os.listdir(work_dir)
                if not items:  # Directory is empty
                    import shutil
                    for item in os.listdir(shared_notebooks):
                        src = os.path.join(shared_notebooks, item)
                        dst = os.path.join(work_dir, item)
                        if os.path.isdir(src):
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                    # Set ownership after copying
                    try:
                        import subprocess
                        subprocess.run(['chown', '-R', f'{username}:users', work_dir], check=False)
                    except:
                        pass
            except Exception as e:
                print(f"Warning: Could not copy shared notebooks: {e}")
        
        return work_dir
    
    def get_env(self):
        """Get environment variables for the spawner"""
        env = super().get_env()
        # Add shared data path
        env['SHARED_DATA'] = '/shared/data'
        return env

c.JupyterHub.spawner_class = CustomLocalProcessSpawner

# Run as the user (not root)
# This requires the user to exist in the system
c.LocalProcessSpawner.set_user = True

# Default URL for users
c.Spawner.default_url = '/lab'

# Command to start single-user server
c.LocalProcessSpawner.cmd = ['jupyter-labhub']

# Environment variables to pass to spawned notebooks
c.Spawner.environment = {
    'MYSQL_HOST': os.getenv('MYSQL_HOST', 'mysql'),
    'MYSQL_PORT': os.getenv('MYSQL_PORT', '3306'),
    'MYSQL_DATABASE': os.getenv('MYSQL_DATABASE', 'beer_db'),
    'MYSQL_USER': os.getenv('MYSQL_USER', 'student'),
    'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'student123'),
    'REDIS_HOST': os.getenv('REDIS_HOST', 'redis'),
    'REDIS_PORT': os.getenv('REDIS_PORT', '6379'),
    'QDRANT_HOST': os.getenv('QDRANT_HOST', 'qdrant'),
    'QDRANT_PORT': os.getenv('QDRANT_PORT', '6333'),
    'VESPA_HOST': os.getenv('VESPA_HOST', 'vespa'),
    'VESPA_PORT': os.getenv('VESPA_PORT', '8080'),
    'SPARK_MASTER': os.getenv('SPARK_MASTER', 'spark://spark-master:7077'),
    'S3_ENDPOINT': os.getenv('S3_ENDPOINT', 'http://minio:9000'),
    'S3_ACCESS_KEY': os.getenv('S3_ACCESS_KEY', 'minioadmin'),
    'S3_SECRET_KEY': os.getenv('S3_SECRET_KEY', 'minioadmin123'),
}

# ============================================================================
# Admin and Services
# ============================================================================

# Admin access to all user notebooks
c.JupyterHub.admin_access = True

# Services (none required for basic setup)
c.JupyterHub.services = []

# ============================================================================
# Logging
# ============================================================================

c.JupyterHub.log_level = 'INFO'
c.Spawner.debug = False

# ============================================================================
# Idle Culler (optional - helps manage resources)
# ============================================================================

# Cull idle servers after 1 hour
c.JupyterHub.load_roles = [
    {
        "name": "idle-culler",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": ["idle-culler"],
    }
]

# Note: To enable idle culler, install jupyterhub-idle-culler and add service configuration

