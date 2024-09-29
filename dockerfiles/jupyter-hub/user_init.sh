#!/bin/bash
PASSWORD="iaas"
USERNAME="iaas"
useradd -u 1000 -g 1000 -m --shell /bin/bash "$USERNAME"
echo "$USERNAME:$PASSWORD" | chpasswd

# Set generic password
PASSWORD="azerty"

# Path to the file containing the usernames
USER_FILE="./users.txt"

# Loop through each line in the file
while IFS= read -r USERNAME
do
  # Check if username is non-empty
  if [ -n "$USERNAME" ]; then
    # Create the user with home directory (-m) and default shell (/bin/bash)
    useradd -m --shell /bin/bash "$USERNAME"
    
    # Set the user's password to 'azerty'
    echo "$USERNAME:$PASSWORD" | chpasswd
    
    echo "Created user $USERNAME with password $PASSWORD"
  fi
done < "$USER_FILE"

