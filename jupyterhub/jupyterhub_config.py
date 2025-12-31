"""
JupyterHub configuration - Simple PAMAuthenticator setup

Note: This file is executed by JupyterHub at runtime.
The 'c' object is automatically provided by JupyterHub's configuration system.
"""
import os

# JupyterHub configuration - Simple PAMAuthenticator setup

# ============================================================================
# General Configuration
# ============================================================================

c.JupyterHub.bind_url = 'http://0.0.0.0:8000'

# ============================================================================
# Authentication - PAMAuthenticator (uses Linux system users)
# ============================================================================

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.Authenticator.allow_all = True

# Allow PAM to handle system users
c.PAMAuthenticator.open_sessions = False

# Load admin users from users.txt (users marked with '*' suffix)
def load_admin_users():
    """Load admin users from users.txt file"""
    admin_users = set()
    users_file = os.getenv('USERS_FILE', '/srv/jupyterhub/users.txt')
    
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if line.endswith('*'):
                            username = line[:-1].strip()
                            if username:
                                admin_users.add(username)
        except Exception as e:
            print(f"Warning: Could not load admin users from {users_file}: {e}")
    
    if not admin_users:
        admin_users.add('admin')
    
    return admin_users

c.Authenticator.admin_users = load_admin_users()

# ============================================================================
# Spawner Configuration - Simple and straightforward
# ============================================================================

# Default URL - JupyterLab
c.Spawner.default_url = '/lab'

# Allow running Jupyter server as root (required since container runs as root for user management)
c.Spawner.args = ['--allow-root']

# Environment variables for data engineering tools
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
    'SHARED_DATA': '/shared/data',
}

# ============================================================================
# Admin Configuration
# ============================================================================

c.JupyterHub.admin_access = True

# ============================================================================
# Logging
# ============================================================================

c.JupyterHub.log_level = 'INFO'
