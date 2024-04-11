#!/bin/bash

# Get the name of the virtual environment
env_name="$1"

if [ -z "$env_name"]; then
  echo "No virtual environement specified, using default: 'venv'"
  env_name="venv"
fi

# Check if the virtual environment directory exists
if [ ! -d "$env_name" ]; then
  echo "The virtual environment '$env_name' does not exist."
  python3 -m venv ./"$env_name"
fi

# Check if the virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "The virtual environment '$env_name' is not active."
  source "$env_name"/bin/activate
fi

python -m pip install -r requirements.txt

python manage.py runserver 0.0.0.0:80
