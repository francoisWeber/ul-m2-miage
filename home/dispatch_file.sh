#!/bin/bash

# Path to the passwords file
PASSWORDS_FILE="/home/francois/passwords.txt"

# Path to the file to copy
SOURCE_FILE="/home/francois/3 exercices/09-project.ipynb"


# Check if the source file exists
if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "Error: Source file '$SOURCE_FILE' does not exist."
    exit 1
fi

# Loop through each line of the passwords file
while IFS=" - " read -r username password; do
    # Check if the user exists on the system
    if id "$username" &>/dev/null; then
        # Define the destination path
        DEST_FILE="/home/$username/09-project.ipynb"

        # Copy the file to the user's home directory
        cp "$SOURCE_FILE" "$DEST_FILE"

        # Change ownership to the user and set permissions
        chown "$username:$username" "$DEST_FILE"
        chmod 700 "$DEST_FILE"

        echo "File copied and permissions set for user: $username"
    else
        echo "Warning: User '$username' does not exist on the system."
    fi
done < "$PASSWORDS_FILE"
