#!/bin/bash

# Install system dependencies
echo "Updating package lists..."
apt-get update -qq

echo "Installing system dependencies..."
apt-get install -y --no-install-recommends \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    python3-pip \
    gcc \
    g++ \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*
    python3-venv

# Create and activate virtual environment
python3 -m venv /home/adminuser/venv
source /home/adminuser/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install any additional packages that might be needed
pip install pyarrow  # Required for pandas on some systems

echo "Setup completed successfully"
