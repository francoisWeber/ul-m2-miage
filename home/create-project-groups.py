import json
import os
import subprocess

# Load the JSON file
with open('projects.json', 'r') as f:
    projects = json.load(f)

base_path = "/some/path"

# Iterate through projects and set group permissions
for project, users in projects.items():
    group_name = project
    file_path = os.path.join(base_path, f"{project}.sd")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist. Skipping.")
        continue

    # Change group ownership of the file
    try:
        subprocess.run(['sudo', 'chgrp', group_name, file_path], check=True)
        print(f"Group ownership of '{file_path}' changed to '{group_name}'.")
    except subprocess.CalledProcessError:
        print(f"Failed to change group ownership for '{file_path}'.")

    # Set read-write permissions for the group
    try:
        subprocess.run(['sudo', 'chmod', '660', file_path], check=True)
        print(f"Permissions for '{file_path}' set to '660' (RW for owner and group).")
    except subprocess.CalledProcessError:
        print(f"Failed to set permissions for '{file_path}'.")
