#!/bin/bash

# Define the virtual environment directory
ENV_DIR="venv"

# Create the virtual environment
echo "Creating virtual environment..."
python -m venv $ENV_DIR

# Check if virtual environment creation succeeded
if [ ! -d "$ENV_DIR/Scripts" ]; then
  echo "Failed to create virtual environment. Exiting."
  exit 1
fi

# Activate the virtual environment
echo "Installing dependencies..."
source $ENV_DIR/Scripts/activate

# Install requirements
python -m pip install --upgrade pip setuptools wheel

python -m pip install --upgrade pip
python -m pip install setuptools

python -m pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Virtual environment setup complete."
