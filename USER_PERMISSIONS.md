# User Permissions and Home Directory Setup

## Overview

The JupyterHub setup ensures that each user has:
- ✅ Read-Write (RW) access to their own `/home/{username}` directory
- ✅ Ability to start Jupyter environments
- ✅ Isolated workspace in `/home/{username}/work`
- ✅ Access to shared data via symlink

## How It Works

### 1. Linux User Account Creation

When the container starts, `create_linux_users.py` creates Linux user accounts for each user in `users.txt`:

- Creates user account: `useradd -m -s /bin/bash -G users {username}`
- Creates home directory: `/home/{username}`
- Creates work directory: `/home/{username}/work`
- Sets ownership: `chown -R {username}:users /home/{username}`
- Sets permissions: `chmod 755` (user RWX, group RX, others RX)

### 2. JupyterHub Spawner Configuration

The `CustomLocalProcessSpawner`:
- Runs each user's Jupyter server as that Linux user (not root)
- Sets notebook directory to `/home/{username}/work`
- Ensures proper permissions before spawning
- Copies shared notebooks on first use

### 3. Volume Mounting

```yaml
volumes:
  - jupyterhub_home:/home  # Persistent, RW for each user
  - ./notebooks:/shared/notebooks:ro  # Shared templates (read-only)
  - ./beer-dataset:/shared/data:ro    # Shared dataset (read-only)
```

## Directory Structure

```
/home/
├── admin/              # Admin user's home
│   ├── work/          # Notebooks (RW)
│   └── data -> /shared/data  # Symlink to shared data
├── student1/           # Student 1's home
│   ├── work/          # Notebooks (RW)
│   └── data -> /shared/data
└── student2/          # Student 2's home
    ├── work/          # Notebooks (RW)
    └── data -> /shared/data

/shared/
├── notebooks/         # Template notebooks (read-only)
└── data/              # Shared dataset (read-only)
```

## Permissions

### Home Directory (`/home/{username}`)
- **Owner**: `{username}:users`
- **Permissions**: `755` (rwxr-xr-x)
- **User can**: Read, write, execute
- **Group can**: Read, execute
- **Others can**: Read, execute

### Work Directory (`/home/{username}/work`)
- **Owner**: `{username}:users`
- **Permissions**: `755` (rwxr-xr-x)
- **User can**: Create, edit, delete notebooks
- **Isolated**: Each user's work is separate

### Shared Directories
- `/shared/notebooks`: Read-only templates
- `/shared/data`: Read-only dataset

## User Isolation

Each user:
- ✅ Has their own Linux account
- ✅ Runs Jupyter as their own user (not root)
- ✅ Has isolated `/home/{username}/work` directory
- ✅ Cannot access other users' home directories
- ✅ Can read shared data via `/home/{username}/data` symlink

## Verification

### Check User Creation

```bash
# List all users
docker-compose exec jupyterhub getent passwd | grep -E '^(admin|student)'

# Check user's home directory
docker-compose exec jupyterhub ls -la /home/

# Check permissions
docker-compose exec jupyterhub ls -ld /home/student1
docker-compose exec jupyterhub ls -ld /home/student1/work
```

### Test User Access

1. Login as a user via JupyterHub web interface
2. Create a new notebook in their workspace
3. Save files - should work without permission errors
4. Check file ownership:
   ```python
   import os
   print(os.getcwd())  # Should be /home/{username}/work
   print(os.getuid())  # Should be user's UID (not 0/root)
   ```

## Troubleshooting

### Permission Denied Errors

If users can't write to their home directory:

```bash
# Fix ownership
docker-compose exec jupyterhub chown -R student1:users /home/student1

# Fix permissions
docker-compose exec jupyterhub chmod 755 /home/student1
docker-compose exec jupyterhub chmod 755 /home/student1/work
```

### User Can't Start Jupyter

1. Verify user exists:
   ```bash
   docker-compose exec jupyterhub id student1
   ```

2. Check spawner logs:
   ```bash
   docker-compose logs jupyterhub | grep spawn
   ```

3. Verify user has home directory:
   ```bash
   docker-compose exec jupyterhub test -d /home/student1 && echo "OK" || echo "Missing"
   ```

### Reset User Permissions

```bash
# Stop JupyterHub
docker-compose stop jupyterhub

# Fix all user permissions
docker-compose exec jupyterhub bash -c "
  for user in \$(getent passwd | cut -d: -f1 | grep -E '^(admin|student)'); do
    chown -R \$user:users /home/\$user
    chmod 755 /home/\$user
    chmod 755 /home/\$user/work
  done
"

# Restart
docker-compose start jupyterhub
```

## Security Notes

- ✅ Users run as non-root (their own Linux user)
- ✅ Users cannot access other users' directories
- ✅ Shared data is read-only
- ✅ Each user's work is isolated
- ⚠️ Container runs as root to allow user creation (required for LocalProcessSpawner)
- ⚠️ For production, consider using DockerSpawner for better isolation

## Adding New Users

When you add a user to `users.txt`:

1. Edit `jupyterhub/users.txt`
2. Restart JupyterHub: `docker-compose restart jupyterhub`
3. The system will:
   - Create Linux user account
   - Create home directory with proper permissions
   - Create work directory
   - Add user to JupyterHub database
   - Generate password

The new user will have full RW access to `/home/{username}/work` automatically!

