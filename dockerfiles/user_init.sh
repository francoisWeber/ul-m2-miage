#!/bin/bash

# Array of users to be created
USERS=("user1" "user2" "francois.weber")

# Passwords for the users
PASSWORDS=("password1" "password2" "azerty")

for i in "${!USERS[@]}"; do
  username="${USERS[$i]}"
  password="${PASSWORDS[$i]}"

  # Check if user already exists
  if id "$username" &>/dev/null; then
    echo "User $username already exists."
  else
    # Create the user and set the password
    useradd -m "$username"
    echo "$username:$password" | chpasswd
    echo "User $username created."
  fi
done
