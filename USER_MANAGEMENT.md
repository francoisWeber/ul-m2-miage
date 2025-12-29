# User Management System

## Overview

The JupyterHub setup includes an automated user management system that creates users from a `users.txt` file when the container starts.

## How It Works

1. **`users.txt`** - Contains the list of users (one per line)
   - Add `*` after username to make them admin
   - Example: `admin*` creates an admin user named `admin`

2. **`create_users.py`** - Python script that:
   - Reads `users.txt`
   - Generates random passwords (12 characters)
   - Creates users in the JupyterHub SQLite database
   - Saves credentials to `users_pass.txt`

3. **`entrypoint.sh`** - Runs before JupyterHub starts:
   - Executes `create_users.py` if `users.txt` exists
   - Then starts JupyterHub

4. **`jupyterhub_config.py`** - Loads admin users from the database

## Usage

### Step 1: Edit `users.txt`

Edit `jupyterhub/users.txt`:

```
admin*
student1
student2
student3
instructor*
```

### Step 2: Start Services

```bash
./scripts/start.sh
# or
docker-compose up -d
```

### Step 3: Get Passwords

After the container starts, check `jupyterhub/users_pass.txt`:

```bash
cat jupyterhub/users_pass.txt
```

Output:
```
# JupyterHub User Credentials
# Format: username:password [admin]
# Generated automatically - keep this file secure!

admin:Ab3$kL9mN2pQ [admin]
student1:Xy7@mP4qR9sT
student2:Zb5#nQ8rS2tU
student3:Wc6$oR1sT4vW
instructor:Yd7#pS2tU5wX [admin]
```

### Step 4: Distribute Credentials

Share the `users_pass.txt` file with students (securely!).

## Updating Users

### Add New Users

1. Edit `jupyterhub/users.txt`
2. Add new usernames (one per line)
3. Restart: `docker-compose restart jupyterhub`
4. New passwords will be generated

### Change Existing User to Admin

1. Edit `jupyterhub/users.txt`
2. Add `*` after the username: `student1*`
3. Restart: `docker-compose restart jupyterhub`

### Reset All Passwords

```bash
# Stop JupyterHub
docker-compose stop jupyterhub

# Remove database (deletes all users)
docker-compose exec jupyterhub rm /srv/jupyterhub/jupyterhub.sqlite

# Restart (recreates all users with new passwords)
docker-compose start jupyterhub
```

## File Locations

- **Input:** `jupyterhub/users.txt` (edit this)
- **Output:** `jupyterhub/users_pass.txt` (generated automatically)
- **Database:** Stored in Docker volume `jupyterhub_data` at `/srv/jupyterhub/jupyterhub.sqlite`

## Security Notes

⚠️ **Important:**
- `users_pass.txt` contains passwords in plain text
- This file is in `.gitignore` - don't commit it!
- Keep this file secure
- Consider changing passwords after first login
- For production, use stronger authentication (OAuth, LDAP, etc.)

## Troubleshooting

### Users not created?

1. Check if `users.txt` exists: `ls -la jupyterhub/users.txt`
2. Check container logs: `docker-compose logs jupyterhub`
3. Verify file format (one username per line)

### Can't login?

1. Check `users_pass.txt` for correct password
2. Verify username spelling matches `users.txt`
3. Check if user exists in database:
   ```bash
   docker-compose exec jupyterhub sqlite3 /srv/jupyterhub/jupyterhub.sqlite "SELECT name FROM users;"
   ```

### Admin users not working?

1. Verify `*` is after username in `users.txt`
2. Check admin status:
   ```bash
   docker-compose exec jupyterhub sqlite3 /srv/jupyterhub/jupyterhub.sqlite "SELECT name, admin FROM users WHERE admin = 1;"
   ```
3. Restart JupyterHub: `docker-compose restart jupyterhub`
