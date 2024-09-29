#!/bin/bash

# Become root so we can restart desktop managers
if [[ $EUID != 0 ]]; then
  exec pkexec "$(realpath "$0")" "$@"
fi

# Check if the username argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <username>"
  exit 1
fi

# Get the username from the first argument
USERNAME=$1

systemctl enable --now hhd@$USERNAME.service
