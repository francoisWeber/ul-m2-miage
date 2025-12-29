# JupyterHub Configuration

This directory contains the JupyterHub configuration and user management system.

## User Management

### Creating Users from `users.txt`

Users are automatically created from `users.txt` when the container starts.

**Format of `users.txt`:**
```
# Comments start with #
admin*          # Admin user (marked with *)
student1        # Regular user
student2        # Regular user
instructor*     # Another admin user
```

**Rules:**
- One username per line
- Add `*` after username to make them admin
- Lines starting with `#` are ignored
- Empty lines are ignored

### Generated Files

When the container starts, it will:
1. Read `users.txt`
2. Generate random passwords for each user
3. Create users in the JupyterHub database
4. Save credentials to `users_pass.txt`

**`users_pass.txt` format:**
```
# JupyterHub User Credentials
# Format: username:password [admin]
# Generated automatically - keep this file secure!

admin:Ab3$kL9mN2pQ [admin]
student1:Xy7@mP4qR9sT
student2:Zb5#nQ8rS2tU
instructor:Wc6$oR1sT4vW [admin]
```

### Security Notes

- `users_pass.txt` contains passwords in plain text
- This file is automatically added to `.gitignore`
- Keep this file secure and don't commit it to version control
- Consider changing passwords after first login

### Updating Users

To add or modify users:

1. Edit `users.txt`
2. Restart the container: `docker-compose restart jupyterhub`
3. New passwords will be generated for new users
4. Existing users will keep their current passwords (unless you delete the database)

### Resetting All Users

To regenerate all passwords:

```bash
# Stop JupyterHub
docker-compose stop jupyterhub

# Remove the database (this will delete all users)
docker-compose exec jupyterhub rm /srv/jupyterhub/jupyterhub.sqlite

# Restart (users will be recreated from users.txt)
docker-compose start jupyterhub
```

### Manual User Creation

Users can also sign up manually through the web interface if `open_signup` is enabled in `jupyterhub_config.py`.

## Configuration Files

- `Dockerfile` - Builds the JupyterHub image with all dependencies
- `jupyterhub_config.py` - Main JupyterHub configuration
- `create_users.py` - Script that creates users from `users.txt`
- `entrypoint.sh` - Entrypoint script that runs user creation before starting JupyterHub
- `users.txt` - User list (edit this to add/remove users)
- `users_pass.txt` - Generated password file (created automatically)

## Environment Variables

The following environment variables can be set in `docker-compose.yml`:

- `USERS_FILE` - Path to users.txt (default: `/srv/jupyterhub/users.txt`)
- `JUPYTERHUB_DB_PATH` - Path to SQLite database (default: `/srv/jupyterhub/jupyterhub.sqlite`)
- `PASSWORDS_FILE` - Path to output passwords file (default: `/srv/jupyterhub/users_pass.txt`)

