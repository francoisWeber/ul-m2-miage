#!/bin/bash
# # # Setup users and sharing

# Main (useless) user
ADMIN_USER=iaas
PASSWORD=azerty
useradd -u 1001 -g 1001 -m --shell /bin/bash "$ADMIN_USER"
echo "$ADMIN_USER:$PASSWORD" | chpasswd

# Main (mine) user
ADMIN_USER=francois
PASSWORD=1a490110
useradd -u 1000 -g 1000 -m --shell /bin/bash "$ADMIN_USER"
echo "$ADMIN_USER:$PASSWORD" | chpasswd

# # # Other configs # # # #

# Shared config
SHARED_FOLDER="/workshop"
SHARED_GROUP="workshop_group"

DATA_FOLDER="/datasets"

# Users list
USER_FILE="./users.txt"

# User passwords
SALT="sel"
PASSWORD_BACKUP_DIR="/home/iaas/passwords.txt"


# # # # Functions # # # # 
# password generation
generate_password() {
  local username="$1"
  # Generate password: first 8 chars of the salted SHA256 of the username
  echo -n "$SALT $username" | sha256sum | awk '{print substr($1,1,8)}'
}


# # # # SCRIPT # # # # 

# # GROUP CREATION  # #
# Create the shared group if it doesn't exist
if ! getent group "$SHARED_GROUP" > /dev/null; then
  groupadd "$SHARED_GROUP"
  echo "Group $SHARED_GROUP created."
else
  echo "Group $SHARED_GROUP already exists."
fi

# # SHARED FOLDER
# Create the shared folder if it doesn't exist
if [ ! -d "$SHARED_FOLDER" ]; then
  mkdir -p "$SHARED_FOLDER"
  echo "Shared folder $SHARED_FOLDER created."
else
  echo "Shared folder $SHARED_FOLDER already exists."
fi

# # USERS  # #

# Loop through each line in the file
while IFS= read -r USERNAME
do
  # Check if username is non-empty
  if [ -n "$USERNAME" ]; then

    if id "$USERNAME" &>/dev/null; then
      echo "User $USERNAME already exists."
    else
      # Create the user with home directory (-m) and default shell (/bin/bash)
      useradd -m --shell /bin/bash "$USERNAME"
    fi

    password=$(generate_password "$USERNAME")
    
    # Set the user's password to 'azerty'
    echo "$USERNAME:$password" | chpasswd
    
    echo "Created user $USERNAME with password $password"
    echo "$USERNAME - $password" >> $PASSWORD_BACKUP_DIR

    # Add user to workshop group
    usermod -a -G "$SHARED_GROUP" "$USERNAME"

    # simlink the workshop folder 
    ln -sf "$SHARED_FOLDER" "/home/$USERNAME/workshop"
  fi
done < "$USER_FILE"

mv $PASSWORD_BACKUP_DIR /home/iaas/passwords.txt
chown iaas /home/iaas/passwords.txt


# Set ownership and permissions for the shared folder
chown $ADMIN_USER:$SHARED_GROUP "$SHARED_FOLDER"

chmod 770 "$SHARED_FOLDER"
